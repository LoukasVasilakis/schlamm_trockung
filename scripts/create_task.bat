@echo off
setlocal

set TASK_NAME="RunDataImport"
set BATCH_PATH="%~dp0run_import.bat"

schtasks /Create ^
 /TN "%TASK_NAME%" ^
 /TR "%BATCH_PATH%" ^
 /SC DAILY ^
 /ST 00:00 ^
 /F

echo Task "%TASK_NAME%" wurde erstellt.
endlocal