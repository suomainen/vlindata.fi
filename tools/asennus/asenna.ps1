<#
.SYNOPSIS
  Asentaa vlindata.fi-sivutyökalun: Git, Python ja WinSCP (winget), hakee sivuston
  GitHubista ja tekee työpöydälle pikakuvakkeen "VLiNdATA-sivut".

.DESCRIPTION
  Aja kerran tiedostolla asenna.bat. Ennen asennusta:
  - sinulla on GitHub-tunnus ja Oskari on lisännyt sinut repoon suomainen/vlindata.fi
  - tiedät Domainhotellin FTP-tunnukset (tallennetaan vain WinSCP:hen tälle koneelle)
  Asennuksen voi ajaa uudelleen; jo asennetut osat ohitetaan.
#>
$ErrorActionPreference = 'Stop'
$repo = 'https://github.com/suomainen/vlindata.fi.git'

function Otsikko($t) { Write-Host ''; Write-Host "== $t ==" -ForegroundColor Cyan }
function PaivitaPolku {
  $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
}
function Loytyy($komento) { [bool](Get-Command $komento -ErrorAction SilentlyContinue) }
function PythonOk { try { (& python --version 2>&1) -match 'Python 3' } catch { $false } }

Otsikko '1/4 Ohjelmat (Git, Python, WinSCP)'
$winget = Loytyy 'winget'
$ohjelmat = @(
  @{ Nimi = 'Git'; Id = 'Git.Git'; Ok = { Loytyy 'git' } },
  @{ Nimi = 'Python'; Id = 'Python.Python.3.12'; Ok = { PythonOk } },
  @{ Nimi = 'WinSCP'; Id = 'WinSCP.WinSCP'; Ok = {
      (Test-Path "${env:ProgramFiles(x86)}\WinSCP\WinSCP.com") -or (Test-Path "$env:ProgramFiles\WinSCP\WinSCP.com") -or
      (Test-Path "$env:LOCALAPPDATA\Programs\WinSCP\WinSCP.com") } }
)
foreach ($o in $ohjelmat) {
  if (& $o.Ok) { Write-Host "$($o.Nimi): asennettu"; continue }
  if (-not $winget) {
    Write-Host "$($o.Nimi) puuttuu, eikä wingetiä löytynyt. Asenna käsin: git-scm.com, python.org (ruksi 'Add python.exe to PATH'), winscp.net. Aja sitten asennus uudelleen." -ForegroundColor Yellow
    exit 1
  }
  Write-Host "Asennetaan $($o.Nimi)..."
  winget install -e --id $o.Id --accept-package-agreements --accept-source-agreements --silent
  PaivitaPolku
}
PaivitaPolku
if (-not (Loytyy 'git')) { Write-Host 'Git asentui, mutta sitä ei vielä löydy. Käynnistä kone uudelleen ja aja asennus uudestaan.' -ForegroundColor Yellow; exit 1 }
if (-not (PythonOk)) { Write-Host 'Python ei vielä toimi. Käynnistä kone uudelleen ja aja asennus uudestaan.' -ForegroundColor Yellow }

Otsikko '2/4 Sivuston haku GitHubista'
$oletus = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'vlindata.fi'
$kansio = Read-Host "Kansio sivustolle (Enter = $oletus)"
if (-not $kansio) { $kansio = $oletus }
if (Test-Path (Join-Path $kansio '.git')) {
  Write-Host 'Sivusto on jo koneella, haku ohitetaan.'
} else {
  Write-Host 'Haetaan... (GitHub voi pyytää kirjautumista selaimessa: valitse "Sign in with your browser")'
  git clone -c core.autocrlf=false -c core.filemode=false $repo $kansio
  if ($LASTEXITCODE -ne 0) { Write-Host 'Haku epäonnistui. Onko Oskari lisännyt GitHub-tunnuksesi repoon?' -ForegroundColor Red; exit 1 }
}

Otsikko '3/4 Nimi muutoshistoriaan'
$nimi = (git -C $kansio config user.name)
if (-not $nimi) { $nimi = Read-Host 'Nimesi (esim. Virpi Lindvall)' }
$email = (git -C $kansio config user.email)
if (-not $email) { $email = Read-Host 'Sähköpostiosoitteesi' }
git -C $kansio config user.name "$nimi"
git -C $kansio config user.email "$email"
git -C $kansio config core.autocrlf false
git -C $kansio config core.filemode false
git -C $kansio config pull.rebase true

Otsikko '4/4 Pikakuvake ja WinSCP'
$kuvake = Join-Path ([Environment]::GetFolderPath('Desktop')) 'VLiNdATA-sivut.lnk'
$wsh = New-Object -ComObject WScript.Shell
$lnk = $wsh.CreateShortcut($kuvake)
$lnk.TargetPath = Join-Path $kansio 'Sivutyokalu.bat'
$lnk.WorkingDirectory = $kansio
$lnk.IconLocation = (Join-Path $kansio 'favicon.ico')
$lnk.WindowStyle = 7
$lnk.Save()
Write-Host "Työpöydälle tehtiin pikakuvake: VLiNdATA-sivut"

Write-Host ''
Write-Host 'Viimeinen vaihe: tallenna palvelinyhteys WinSCP:hen (vain kerran):' -ForegroundColor Cyan
Write-Host '  1. WinSCP aukeaa. Valitse "Uusi sivusto".'
Write-Host '  2. Tiedostoprotokolla: FTP, Salaus: TLS/SSL Explicit encryption (tai SFTP, jos Oskari niin neuvoo).'
Write-Host '  3. Palvelin, käyttäjätunnus ja salasana Domainhotellin tiedoista.'
Write-Host '  4. Paina "Tallenna", nimeksi vlindata ja ruksi "Tallenna salasana".'
Write-Host '  5. Paina "Kirjaudu" ja hyväksy palvelimen varmenne. Sulje WinSCP.'
$winscp = @("${env:ProgramFiles(x86)}\WinSCP\WinSCP.exe", "$env:ProgramFiles\WinSCP\WinSCP.exe", "$env:LOCALAPPDATA\Programs\WinSCP\WinSCP.exe") |
  Where-Object { Test-Path $_ } | Select-Object -First 1
if ($winscp) { Start-Process $winscp }
Write-Host ''
Write-Host 'Valmis! Avaa työkalu työpöydän kuvakkeesta VLiNdATA-sivut.' -ForegroundColor Green
