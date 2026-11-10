<#
.SYNOPSIS
  Muodostaa commit-viestin automaattisesti (käyttää julkaise.bat).

.DESCRIPTION
  Otsikko tulee CHANGELOG.md:n uusimmasta versiosta, jos se on sama kuin
  js/menu.js:n SITE_VERSION eikä versiolle ole vielä tagia:
  "vlindata.fi 2.6.3: <muutoslokin ensimmäinen kohta>".
  Muuten otsikko on "vlindata.fi: ylläpito (N tiedostoa)". Runkoon tulee
  muutettujen tiedostojen luettelo. Viesti kirjoitetaan tiedostoon UTF-8:na.
#>
param([Parameter(Mandatory = $true)][string]$Tiedosto)

$ErrorActionPreference = "Stop"
$juuri = Split-Path -Parent $PSScriptRoot
Push-Location $juuri
try {
  $versio = ""
  $m = Select-String -Path "js\menu.js" -Pattern "SITE_VERSION = '([0-9.]+)'" | Select-Object -First 1
  if ($m) { $versio = $m.Matches[0].Groups[1].Value }

  $rivit = Get-Content "CHANGELOG.md" -Encoding UTF8
  $kohta = ""
  $otsikko = $rivit | Select-String -Pattern '^## (.+)$' | Select-Object -First 1
  # Muutoslokin kohta vain, jos versio on uusi (tagia ei vielä ole)
  git rev-parse -q --verify "refs/tags/v$versio" *> $null
  $uusiVersio = ($LASTEXITCODE -ne 0)
  if ($uusiVersio -and $otsikko -and $otsikko.Matches[0].Groups[1].Value.Trim() -eq $versio) {
    $kohta = $rivit[$otsikko.LineNumber..($rivit.Count - 1)] |
      Where-Object { $_ -match '^\s*-\s+' } | Select-Object -First 1
    $kohta = ($kohta -replace '^\s*-\s+', '' -replace '`', '').Trim()
    if ($kohta.Length -gt 90) { $kohta = $kohta.Substring(0, 87).TrimEnd() + "..." }
  }

  $tiedostot = @(git diff --cached --name-status)
  if ($kohta) { $aihe = "vlindata.fi ${versio}: $kohta" }
  else { $aihe = "vlindata.fi: ylläpito ($($tiedostot.Count) tiedostoa)" }

  $viesti = @($aihe, "", "Muuttuneet tiedostot:") + ($tiedostot | ForEach-Object { "  $_" })
  [System.IO.File]::WriteAllText($Tiedosto, ($viesti -join "`n") + "`n", (New-Object System.Text.UTF8Encoding($false)))
  Write-Host "Commit-viesti: $aihe"
} finally { Pop-Location }
