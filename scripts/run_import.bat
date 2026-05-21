@echo off
setlocal

REM Projektverzeichnis (Skript liegt in scripts/, also eine Ebene hoch)
cd /d "%~dp0.."

REM Log-Datei im Projektverzeichnis erstellen
set LOG=import.log

echo [%date% %time%] START >> %LOG%

REM Python mit uv ausführen, falls verfügbar, sonst standard python
uv run db/sqlite/load_new_files.py >> %LOG% 2>&1

echo [%date% %time%] END >> %LOG%

endlocal