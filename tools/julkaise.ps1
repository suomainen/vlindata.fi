<#
.SYNOPSIS
  Julkaisee vlindata.fi-sivuston Domainhotellin kotisivutilaan WinSCP:llä.

.DESCRIPTION
  Siirtää repon sivustotiedostot palvelimen juurikansioon (oletus /).
  Vain muuttuneet tiedostot siirretään. Tunnuksia ei ole tässä tiedostossa:
  skripti käyttää WinSCP:hen tallennettua yhteyttä (oletusnimi "vlindata").

  Ylläpitotiedostoja (tools/, .git/, README.md, CHANGELOG.md ...) ei siirretä.

.EXAMPLE
  .\tools\julkaise.ps1 -Esikatselu      # näyttää mitä siirtyisi, ei muuta mitään
  .\tools\julkaise.ps1 -Varmuuskopio    # lataa palvelimen nykyiset tiedostot koneelle
  .\tools\julkaise.ps1                  # julkaisee (ei poista palvelimelta mitään)
  .\tools\julkaise.ps1 -Poista          # julkaisee ja poistaa palvelimelta tiedostot,
                                        # joita ei ole repossa (esim. vanhan sivun jäänteet)
#>
param(
  [string]$Istunto = "vlindata",        # WinSCP:hen tallennetun yhteyden nimi
  [string]$Etakansio = "/",  # sivuston juurikansio palvelimella
  [switch]$Esikatselu,
  [switch]$Poista,
  [switch]$Varmuuskopio,
  [switch]$Pakota                       # julkaise, vaikka repossa olisi tallentamattomia muutoksia
)

$ErrorActionPreference = "Stop"
$juuri = Split-Path -Parent $PSScriptRoot

# Ei siirretä eikä poisteta palvelimelta. Palvelimen omat kansiot (.well-known, cgi-bin)
# ovat listassa, jotta -Poista ei koske niihin.
$ohitettavat = ".git/; tools/; README.md; CHANGELOG.md; .gitignore; .nojekyll; *.bat; .well-known/; cgi-bin/; .user.ini; error_log"

# --- WinSCP ----------------------------------------------------------------
$winscp = @(
  "${env:ProgramFiles(x86)}\WinSCP\WinSCP.com",
  "$env:ProgramFiles\WinSCP\WinSCP.com",
  "$env:LOCALAPPDATA\Programs\WinSCP\WinSCP.com"
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $winscp) {
  $komento = Get-Command WinSCP.com -ErrorAction SilentlyContinue
  if ($komento) { $winscp = $komento.Source }
}
if (-not $winscp) { throw "WinSCP.com ei löytynyt. Asenna WinSCP: https://winscp.net/" }

# --- Repon tila -------------------------------------------------------------
Push-Location $juuri
try {
  $muutokset = git status --porcelain
  $versio = (git describe --tags --always 2>$null)
} finally { Pop-Location }

if ($muutokset -and -not $Pakota -and -not $Esikatselu -and -not $Varmuuskopio) {
  Write-Warning "Repossa on tallentamattomia muutoksia:"
  $muutokset | ForEach-Object { Write-Host "  $_" }
  throw "Tee ensin commit, tai aja uudelleen valitsimella -Pakota."
}

$loki = Join-Path $env:TEMP "vlindata-julkaisu.log"
$komennot = @("option batch abort", "option confirm off", "open $Istunto")

if ($Varmuuskopio) {
  $kohde = Join-Path (Split-Path -Parent $juuri) ("vlindata-varmuuskopio\" + (Get-Date -Format "yyyy-MM-dd_HHmm"))
  New-Item -ItemType Directory -Force -Path $kohde | Out-Null
  Write-Host "Ladataan palvelimen tiedostot kansioon $kohde"
  $komennot += "get -preservetime ""$Etakansio/*"" ""$kohde\"""
} else {
  $valinnat = @()
  if ($Esikatselu) { $valinnat += "-preview" }
  if ($Poista)     { $valinnat += "-delete" }
  $komennot += "synchronize remote $($valinnat -join ' ') -criteria=either -filemask=""| $ohitettavat"" ""$juuri"" ""$Etakansio"""
  if ($Esikatselu) { Write-Host "ESIKATSELU: palvelimelle ei muuteta mitään." }
  Write-Host "Julkaistaan versio $versio -> $Istunto`:$Etakansio"
}
$komennot += "exit"

# Komennot kirjoitetaan väliaikaiseen skriptitiedostoon, jotta lainausmerkit säilyvät oikein
$skripti = Join-Path $env:TEMP "vlindata-julkaisu.txt"
$komennot | Out-File -FilePath $skripti -Encoding utf8
& $winscp /log="$loki" /loglevel=0 /script="$skripti"
$tulos = $LASTEXITCODE
Remove-Item $skripti -ErrorAction SilentlyContinue

if ($tulos -eq 0) {
  if ($Varmuuskopio) { Write-Host "Varmuuskopio valmis." -ForegroundColor Green }
  elseif ($Esikatselu) { Write-Host "Esikatselu valmis. Julkaise ajamalla skripti ilman -Esikatselu-valitsinta." -ForegroundColor Green }
  else { Write-Host "Julkaistu: https://vlindata.fi/ (versio $versio). Päivitä selain (Ctrl+F5)." -ForegroundColor Green }
} else {
  Write-Host "Julkaisu epäonnistui (koodi $tulos). Loki: $loki" -ForegroundColor Red
  exit $tulos
}
