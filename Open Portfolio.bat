@echo off
setlocal
cd /d "%~dp0"

where npm.cmd >nul 2>nul
if errorlevel 1 (
  echo Node.js and npm were not found. Install the LTS version from https://nodejs.org/ and reopen this file.
  pause
  exit /b 1
)

if not exist "node_modules\" (
  echo Installing portfolio dependencies...
  call npm.cmd install
  if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
  )
)

call npm.cmd run dev -- --open
endlocal
