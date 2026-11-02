@echo off
setlocal
cd /d "%~dp0"
echo AXEZENT Beats for Sale - local website preview
echo.
echo Starting on http://127.0.0.1:8080
echo If the browser doesn't open automatically, copy the address above.
echo Do not use this local preview to collect payments or distribute paid audio.
echo.
where py >nul 2>nul
if %errorlevel% equ 0 (
  start "" "http://127.0.0.1:8080"
  py -m http.server 8080 --bind 127.0.0.1
) else (
  where python >nul 2>nul
  if %errorlevel% equ 0 (
    start "" "http://127.0.0.1:8080"
    python -m http.server 8080 --bind 127.0.0.1
  ) else (
    echo Python 3 is not installed or not on PATH.
    echo Visit https://www.python.org/downloads/ and install Python 3.
    pause
  )
)
endlocal
