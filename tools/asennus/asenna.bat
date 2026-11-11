@echo off
chcp 65001 >nul
rem Asentaa vlindata.fi-sivutyökalun tälle koneelle (ks. OHJE.pdf).
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0asenna.ps1"
pause
