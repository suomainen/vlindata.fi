@echo off
rem Avaa vlindata.fi-sivujen päivitystyökalun (tools\sivutyokalu.ps1).
rem Tiedostoa ei julkaista palvelimelle (julkaise.ps1 ohittaa .bat-tiedostot).
start "" powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%~dp0tools\sivutyokalu.ps1"
