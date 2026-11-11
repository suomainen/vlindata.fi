<#
.SYNOPSIS
  VLiNdATA-sivujen päivitystyökalu (ikkuna isoilla painikkeilla).

.DESCRIPTION
  Tehty Virpille, mutta toimii kenen tahansa koneella, jolla repo on.
  Käynnistetään repon juuren Sivutyokalu.bat-tiedostolla tai työpöydän pikakuvakkeella.

  Painikkeet:
    Hae uusin versio   hakee GitHubista muiden tekemät muutokset (omat muutokset säilyvät)
    Avaa tekstit       avaa kansion tools\sivut (fi = suomi, en = englanti)
    Esikatsele         kokoaa sivut ja avaa ne selaimeen tältä koneelta
    Julkaise           nostaa versionumeron, kirjaa muutoslokin, tallentaa gitiin (commit + tagi),
                       vie GitHubiin ja julkaisee palvelimelle tarkistuksen jälkeen
    Tee zip            tallentaa nykyisen version zip-pakettina työpöydälle

  Versio nousee korjausnumerolla (2.8.2 -> 2.8.3). Isommat versionnostot tekee Oskari.
  Julkaisu käyttää tools\julkaise.ps1:tä ja WinSCP:hen tallennettua yhteyttä "vlindata".
  Tarkempi loki: %TEMP%\vlindata-sivutyokalu.log
#>
param([switch]$EiIkkunaa)  # testikäyttö: vain funktiot, ei ikkunaa

$ErrorActionPreference = 'Stop'
$script:Juuri = Split-Path -Parent $PSScriptRoot
$script:Loki = Join-Path ([IO.Path]::GetTempPath()) 'vlindata-sivutyokalu.log'
$script:Utf8 = New-Object System.Text.UTF8Encoding($false)
$script:Esikatselu = $null       # paikallisen esikatselupalvelimen prosessi
$script:EsikatseluPortti = 8765

# Näitä voi korvata (ikkuna tai testit)
$script:Kirjoita = { param($teksti) Write-Host $teksti }
$script:Kysy = { param($kysymys) $true }
$script:Odota = { }              # pitää ikkunan elossa pitkien komentojen aikana

# ---- Apufunktiot -------------------------------------------------------------
function Kirjoita([string]$teksti) { & $script:Kirjoita $teksti }

function Lokiin([string]$teksti) {
  try { [IO.File]::AppendAllText($script:Loki, ("[{0:HH:mm:ss}] {1}`r`n" -f (Get-Date), $teksti), $script:Utf8) } catch { }
}

function Lainaa([string]$a) {
  if ($a -eq '') { return '""' }
  if ($a -notmatch '[\s"]') { return $a }
  return '"' + ($a -replace '"', '\"') + '"'
}

# Ajaa ohjelman repon kansiossa ja palauttaa @{ Koodi; Tuloste }
function Aja([string]$ohjelma, [string[]]$argumentit) {
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = $ohjelma
  $psi.Arguments = ($argumentit | ForEach-Object { Lainaa $_ }) -join ' '
  $psi.WorkingDirectory = $script:Juuri
  $psi.UseShellExecute = $false
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.CreateNoWindow = $true
  $psi.StandardOutputEncoding = $script:Utf8
  $psi.StandardErrorEncoding = $script:Utf8
  $psi.EnvironmentVariables['GIT_TERMINAL_PROMPT'] = '0'   # kirjautuminen ikkunassa, ei komentorivillä
  $psi.EnvironmentVariables['PYTHONIOENCODING'] = 'utf-8'
  Lokiin "> $ohjelma $($psi.Arguments)"
  $p = [System.Diagnostics.Process]::Start($psi)
  $out = $p.StandardOutput.ReadToEndAsync()
  $err = $p.StandardError.ReadToEndAsync()
  while (-not $p.HasExited) { & $script:Odota; Start-Sleep -Milliseconds 50 }
  $p.WaitForExit()
  $tuloste = ($out.Result + $err.Result).Trim()
  Lokiin "  koodi $($p.ExitCode): $tuloste"
  return @{ Koodi = $p.ExitCode; Tuloste = $tuloste }
}

function Git([string[]]$argumentit) { Aja 'git' $argumentit }

function GitOk([string[]]$argumentit, [string]$virhe) {
  $t = Git $argumentit
  if ($t.Koodi -ne 0) { throw "$virhe`n$($t.Tuloste)" }
  return $t.Tuloste
}

function EtsiPython {
  foreach ($n in @('python', 'py')) {
    try {
      $t = Aja $n @('--version')
      if ($t.Koodi -eq 0 -and $t.Tuloste -match 'Python 3') { return $n }
    } catch { }
  }
  return $null
}

function Kokoa {
  $py = EtsiPython
  if (-not $py) { throw 'Pythonia ei löytynyt. Asenna Python (asennusohje) ja käynnistä työkalu uudelleen.' }
  $t = Aja $py @('tools/rakenna.py')
  if ($t.Koodi -ne 0) { throw "Sivujen kokoaminen epäonnistui. Tarkista viimeksi muuttamasi teksti.`n$($t.Tuloste)" }
}

function Lue([string]$polku) { [IO.File]::ReadAllText((Join-Path $script:Juuri $polku), $script:Utf8) }
function Tallenna([string]$polku, [string]$teksti) { [IO.File]::WriteAllText((Join-Path $script:Juuri $polku), $teksti, $script:Utf8) }

function Versio {
  $m = [regex]::Match((Lue 'js/menu.js'), "SITE_VERSION = '([0-9]+\.[0-9]+\.[0-9]+)'")
  if (-not $m.Success) { throw 'Versionumeroa ei löytynyt tiedostosta js/menu.js.' }
  return $m.Groups[1].Value
}

function TagiOn([string]$v) { (Git @('rev-parse', '-q', '--verify', "refs/tags/v$v")).Koodi -eq 0 }

# Koottavat sivut: kaikki .html-tiedostot paitsi tools/-kansio ja käsin tehty 404.html, sekä sitemap.xml
function KootutTiedostot {
  $t = GitOk @('ls-files') 'Tiedostolistaa ei saatu.'
  return @($t -split "`n" | ForEach-Object { $_.Trim() } |
    Where-Object { ($_ -like '*.html' -and $_ -notlike 'tools/*' -and $_ -ne '404.html') -or $_ -eq 'sitemap.xml' })
}

function OmatMuutokset { @((Git @('status', '--porcelain')).Tuloste -split "`n" | Where-Object { $_.Trim() }) }

# ---- Toiminnot ---------------------------------------------------------------

# Hakee GitHubista uusimman version. Omat muutokset pannaan hetkeksi sivuun ja palautetaan.
# Kootut sivut palautetaan ensin ennalleen, koska ne kootaan lopuksi uudelleen (ei turhia ristiriitoja).
function HaeUusin {
  Kirjoita 'Haetaan uusin versio GitHubista...'
  $t = Git @('fetch', '-q', 'origin')
  if ($t.Koodi -ne 0) { throw "GitHubiin ei saatu yhteyttä. Tarkista verkkoyhteys ja kirjautuminen.`n$($t.Tuloste)" }
  $jaljessa = [int](GitOk @('rev-list', '--count', 'HEAD..origin/main') 'Versioiden vertailu epäonnistui.')
  if ($jaljessa -eq 0) { Kirjoita 'Sinulla on jo uusin versio.'; return }

  $kootut = KootutTiedostot
  if ($kootut.Count) { $null = Git (@('checkout', '--') + $kootut) }
  $sivuun = (OmatMuutokset).Count -gt 0
  if ($sivuun) { GitOk @('stash', 'push', '-u', '-q', '-m', 'sivutyokalu') 'Omien muutosten tallennus sivuun epäonnistui.' | Out-Null }

  $t = Git @('pull', '--rebase', '-q', 'origin', 'main')
  if ($t.Koodi -ne 0) {
    $null = Git @('rebase', '--abort')
    if ($sivuun) { $null = Git @('stash', 'pop', '-q') }
    throw "Uusimman version haku epäonnistui. Ota yhteyttä Oskariin.`n$($t.Tuloste)"
  }
  if ($sivuun) {
    $t = Git @('stash', 'pop', '-q')
    if ($t.Koodi -ne 0) {
      $null = Git @('reset', '--hard', '-q')
      throw ('Oskari on muuttanut samoja kohtia kuin sinä. Omat muutoksesi ovat tallessa (git stash), ' +
             'mutta ne pitää yhdistää käsin. Ota yhteyttä Oskariin äläkä tee uusia muutoksia sillä välin.')
    }
  }
  Kokoa
  Kirjoita "Uusin versio haettu ($jaljessa muutosta). Versio nyt $(Versio)."
}

function NostaVersio([string]$kuvaus) {
  $vanha = Versio
  $osat = $vanha.Split('.')
  $uusi = $vanha
  do { $osat[2] = [string]([int]$osat[2] + 1); $uusi = $osat -join '.' } while (TagiOn $uusi)

  Tallenna 'js/menu.js' ((Lue 'js/menu.js') -replace "SITE_VERSION = '[0-9.]+'", "SITE_VERSION = '$uusi'")
  Tallenna 'tools/rakenna.py' ((Lue 'tools/rakenna.py') -replace 'VERSIO = "[0-9.]+"', "VERSIO = `"$uusi`"")
  $loki = Lue 'CHANGELOG.md'
  $i = $loki.IndexOf("`n## ")
  if ($i -lt 0) { throw 'CHANGELOG.md:n rakenne on muuttunut (versio-otsikkoa ei löytynyt).' }
  $loki = $loki.Substring(0, $i + 1) + "## $uusi`n`n- $kuvaus`n`n" + $loki.Substring($i + 1)
  Tallenna 'CHANGELOG.md' $loki
  return $uusi
}

# Kumoaa viimeisimmän (vielä GitHubiin viemättömän) julkaisucommitin, mutta säilyttää omat tekstimuutokset
function KumoaVersionnosto {
  $null = Git @('reset', '-q', 'HEAD~1')
  $palautettavat = @('js/menu.js', 'tools/rakenna.py', 'CHANGELOG.md') + (KootutTiedostot)
  $null = Git (@('checkout', '--') + $palautettavat)
}

function Julkaise([string]$kuvaus) {
  $kuvaus = ($kuvaus -replace '\s+', ' ').Trim()
  for ($yritys = 1; $yritys -le 2; $yritys++) {
    HaeUusin
    Kokoa
    $muutoksia = (OmatMuutokset).Count -gt 0
    $versio = Versio
    if ($muutoksia) {
      if (-not $kuvaus) { throw 'Kirjoita ensin lyhyesti, mitä muutit (kenttä "Mitä muutit?").' }
      $versio = NostaVersio $kuvaus
      Kokoa
      GitOk @('add', '-A') 'Muutosten tallennus epäonnistui.' | Out-Null
      GitOk @('commit', '-q', '-m', "vlindata.fi ${versio}: $kuvaus") 'Muutosten tallennus (commit) epäonnistui.' | Out-Null
      Kirjoita "Muutokset tallennettu versioksi $versio."
    } else {
      Kirjoita "Ei uusia muutoksia. Julkaistaan nykyinen versio $versio."
    }
    $t = Git @('push', '-q', 'origin', 'HEAD:main')
    if ($t.Koodi -eq 0) { break }
    if ($muutoksia -and $yritys -lt 2) {
      Kirjoita 'Oskari julkaisi juuri samaan aikaan. Yhdistetään ja yritetään uudelleen...'
      KumoaVersionnosto
      continue
    }
    throw "Vienti GitHubiin epäonnistui.`n$($t.Tuloste)"
  }

  if (-not (TagiOn $versio)) {
    GitOk @('tag', '-a', "v$versio", '-m', "vlindata.fi $versio") 'Versiotagin teko epäonnistui.' | Out-Null
  }
  $null = Git @('push', '-q', 'origin', "refs/tags/v$versio")
  Kirjoita "Versio $versio on GitHubissa."

  Kirjoita 'Tarkistetaan, mitkä tiedostot palvelimelle siirtyisivät...'
  $esi = Aja 'powershell' @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'tools\julkaise.ps1', '-Esikatselu')
  if ($esi.Koodi -ne 0) { throw "Yhteys palvelimeen ei onnistunut. Onko WinSCP:ssä tallennettu yhteys nimeltä vlindata?`n$($esi.Tuloste)" }
  $siirrot = @($esi.Tuloste -split "`n" | Where-Object { $_ -match '\.(html|css|js|webp|png|jpg|ico|xml|txt|svg|woff2|webmanifest)\b' })
  Kirjoita "Siirrettäviä tiedostoja noin $($siirrot.Count)."
  if (-not (& $script:Kysy "Julkaistaanko versio $versio sivustolle vlindata.fi?")) {
    Kirjoita 'Julkaisu peruttu. Muutokset ovat GitHubissa; voit julkaista myöhemmin painamalla Julkaise uudelleen.'
    return
  }
  Kirjoita 'Julkaistaan palvelimelle...'
  $t = Aja 'powershell' @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'tools\julkaise.ps1')
  if ($t.Koodi -ne 0) { throw "Julkaisu palvelimelle epäonnistui.`n$($t.Tuloste)" }
  Kirjoita "Valmis! Versio $versio on julkaistu: https://vlindata.fi/ (päivitä selain: Ctrl+F5)."
}

function Esikatsele {
  Kirjoita 'Kootaan sivut...'
  Kokoa
  if (-not $script:Esikatselu -or $script:Esikatselu.HasExited) {
    $py = EtsiPython
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $py
    $psi.Arguments = "-m http.server $script:EsikatseluPortti --bind 127.0.0.1"
    $psi.WorkingDirectory = $script:Juuri
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $script:Esikatselu = [System.Diagnostics.Process]::Start($psi)
    Start-Sleep -Milliseconds 800
  }
  Start-Process "http://localhost:$script:EsikatseluPortti/"
  Kirjoita "Esikatselu avattu selaimeen (http://localhost:$script:EsikatseluPortti/). Muut eivät näe sitä."
}

function TeeZip {
  $v = Versio
  $kansio = [Environment]::GetFolderPath('Desktop')
  if (-not $kansio) { $kansio = [Environment]::GetFolderPath('UserProfile') }
  $kohde = Join-Path $kansio "vlindata-fi-v$v.zip"
  GitOk @('archive', '--format=zip', "--prefix=vlindata-fi-v$v/", '-o', $kohde, 'HEAD') 'Zip-paketin teko epäonnistui.' | Out-Null
  Kirjoita "Zip tallennettu työpöydälle: $kohde"
  if ((OmatMuutokset).Count) { Kirjoita 'Huom: zipissä ei ole vielä julkaisemattomia muutoksiasi.' }
}

function Tila {
  $muutokset = (OmatMuutokset).Count
  $teksti = "Versio $(Versio)"
  if ($muutokset) { $teksti += " · julkaisemattomia muutoksia $muutokset tiedostossa" } else { $teksti += ' · ei julkaisemattomia muutoksia' }
  return $teksti
}

if ($EiIkkunaa) { return }

# ---- Ikkuna -----------------------------------------------------------------
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()

$metsa = [System.Drawing.ColorTranslator]::FromHtml('#344C3C')
$terra = [System.Drawing.ColorTranslator]::FromHtml('#C78F7B')
$pohja = [System.Drawing.ColorTranslator]::FromHtml('#F7F4EC')
$teksti = [System.Drawing.ColorTranslator]::FromHtml('#29362E')
$fontti = New-Object System.Drawing.Font('Segoe UI', 10)

$ikkuna = New-Object System.Windows.Forms.Form
$ikkuna.Text = 'VLiNdATA – sivujen päivitys'
$ikkuna.Size = New-Object System.Drawing.Size(720, 640)
$ikkuna.MinimumSize = New-Object System.Drawing.Size(640, 560)
$ikkuna.StartPosition = 'CenterScreen'
$ikkuna.BackColor = $pohja
$ikkuna.ForeColor = $teksti
$ikkuna.Font = $fontti
$ikoni = Join-Path $script:Juuri 'favicon.ico'
if (Test-Path $ikoni) { try { $ikkuna.Icon = New-Object System.Drawing.Icon($ikoni) } catch { } }

$otsikko = New-Object System.Windows.Forms.Label
$otsikko.Text = 'vlindata.fi – sivujen päivitys'
$otsikko.Font = New-Object System.Drawing.Font('Segoe UI Semibold', 15)
$otsikko.AutoSize = $true
$otsikko.Location = New-Object System.Drawing.Point(20, 16)
$ikkuna.Controls.Add($otsikko)

$tila = New-Object System.Windows.Forms.Label
$tila.AutoSize = $true
$tila.Location = New-Object System.Drawing.Point(22, 54)
$ikkuna.Controls.Add($tila)

function Painike([string]$nimi, [int]$x, [int]$y, [int]$leveys, $vari, $tekstivari) {
  $b = New-Object System.Windows.Forms.Button
  $b.Text = $nimi
  $b.Location = New-Object System.Drawing.Point($x, $y)
  $b.Size = New-Object System.Drawing.Size($leveys, 44)
  $b.FlatStyle = 'Flat'
  $b.FlatAppearance.BorderSize = 0
  $b.BackColor = $vari
  $b.ForeColor = $tekstivari
  $b.Cursor = 'Hand'
  $ikkuna.Controls.Add($b)
  return $b
}

$valkoinen = [System.Drawing.Color]::White
$bHae = Painike '1. Hae uusin versio' 20 88 210 $metsa $valkoinen
$bTekstit = Painike '2. Avaa tekstit' 240 88 210 $metsa $valkoinen
$bEsi = Painike '3. Esikatsele' 460 88 210 $metsa $valkoinen

$ohje = New-Object System.Windows.Forms.Label
$ohje.Text = '4. Mitä muutit? (lyhyesti, näkyy muutoslokissa)'
$ohje.AutoSize = $true
$ohje.Location = New-Object System.Drawing.Point(20, 150)
$ikkuna.Controls.Add($ohje)

$kuvaus = New-Object System.Windows.Forms.TextBox
$kuvaus.Location = New-Object System.Drawing.Point(20, 176)
$kuvaus.Size = New-Object System.Drawing.Size(430, 30)
$kuvaus.Anchor = 'Top, Left, Right'
$ikkuna.Controls.Add($kuvaus)

$bJulkaise = Painike 'Julkaise' 460 170 210 $terra $teksti
$bJulkaise.Anchor = 'Top, Right'
$bJulkaise.Font = New-Object System.Drawing.Font('Segoe UI Semibold', 11)

$bSivu = Painike 'Avaa vlindata.fi' 20 228 210 $pohja $teksti
$bZip = Painike 'Tee zip työpöydälle' 240 228 210 $pohja $teksti
foreach ($b in @($bSivu, $bZip)) { $b.FlatAppearance.BorderSize = 1; $b.FlatAppearance.BorderColor = $metsa }

$viestit = New-Object System.Windows.Forms.TextBox
$viestit.Multiline = $true
$viestit.ReadOnly = $true
$viestit.ScrollBars = 'Vertical'
$viestit.BackColor = [System.Drawing.Color]::White
$viestit.Location = New-Object System.Drawing.Point(20, 290)
$viestit.Size = New-Object System.Drawing.Size(650, 290)
$viestit.Anchor = 'Top, Bottom, Left, Right'
$ikkuna.Controls.Add($viestit)

$script:Kirjoita = {
  param($t)
  $viestit.AppendText(("{0:HH:mm}  {1}" -f (Get-Date), $t) + "`r`n")
  Lokiin $t
  [System.Windows.Forms.Application]::DoEvents()
}
$script:Odota = { [System.Windows.Forms.Application]::DoEvents() }
$script:Kysy = {
  param($k)
  ([System.Windows.Forms.MessageBox]::Show($ikkuna, $k, 'Julkaistaanko?', 'YesNo', 'Question')) -eq 'Yes'
}

$painikkeet = @($bHae, $bTekstit, $bEsi, $bJulkaise, $bSivu, $bZip)
function Suorita([scriptblock]$toiminto) {
  $painikkeet | ForEach-Object { $_.Enabled = $false }
  $ikkuna.Cursor = 'WaitCursor'
  try { & $toiminto }
  catch {
    $viesti = $_.Exception.Message
    Kirjoita "VIRHE: $viesti"
    [System.Windows.Forms.MessageBox]::Show($ikkuna, ($viesti -split "`n")[0], 'Jokin meni pieleen', 'OK', 'Warning') | Out-Null
  }
  finally {
    $painikkeet | ForEach-Object { $_.Enabled = $true }
    $ikkuna.Cursor = 'Default'
    try { $tila.Text = Tila } catch { $tila.Text = '' }
  }
}

$bHae.Add_Click({ Suorita { HaeUusin } })
$bTekstit.Add_Click({ Suorita {
  Start-Process explorer.exe (Join-Path $script:Juuri 'tools\sivut')
  Kirjoita 'Tekstit: kansio fi = suomeksi, en = englanniksi. Avaa tiedosto Muistiolla tai VS Codella, tallenna ja paina Esikatsele.'
} })
$bEsi.Add_Click({ Suorita { Esikatsele } })
$bJulkaise.Add_Click({ Suorita { Julkaise $kuvaus.Text; if ((OmatMuutokset).Count -eq 0) { $kuvaus.Text = '' } } })
$bSivu.Add_Click({ Start-Process 'https://vlindata.fi/' })
$bZip.Add_Click({ Suorita { TeeZip } })

$ikkuna.Add_Shown({
  Suorita {
    foreach ($o in @('git')) { if (-not (Get-Command $o -ErrorAction SilentlyContinue)) { throw 'Gitiä ei löytynyt. Asenna se asennusohjeen mukaan.' } }
    if (-not (EtsiPython)) { Kirjoita 'Huom: Pythonia ei löytynyt. Esikatselu ja julkaisu eivät toimi ennen asennusta.' }
    Kirjoita 'Tervetuloa! Aloita painamalla "1. Hae uusin versio".'
  }
})
$ikkuna.Add_FormClosed({ if ($script:Esikatselu -and -not $script:Esikatselu.HasExited) { try { $script:Esikatselu.Kill() } catch { } } })

[void]$ikkuna.ShowDialog()
