@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
title AXEZENT - OWN WINDOWS MUSIC WEBSITE

echo ==================================================
echo AXEZENT - BEATS AND INSTRUMENTALS FOR SALE
echo Owner-operated Windows music website
echo ==================================================
echo.

REM Do NOT put the 50 review MP3 files in this public GitHub repository.
set "AXEZENT_PREVIEW_DIR=%~dp0..\..\AXEZENT_PRIVATE_TAGGED_PREVIEWS"
if not exist "%AXEZENT_PREVIEW_DIR%" (
  echo The 50 private tagged MP3s must be in:
  echo "%AXEZENT_PREVIEW_DIR%"
  echo Create/extract this folder next to the repository.
  pause
  exit /b 1
)
where py >nul 2>nul
if not errorlevel 1 (
  set "PYTHON_CMD=py -3"
  goto CHECK_AUDIO
)
where python >nul 2>nul
if not errorlevel 1 (
  set "PYTHON_CMD=python"
  goto CHECK_AUDIO
)
echo ERROR: Python 3 is not installed, or is missing from PATH.
echo Python is the only runtime needed for the local first-party audio API.
pause
exit /b 1

:CHECK_AUDIO
%PYTHON_CMD% scripts\check_owned_preview_library.py --preview-dir "%AXEZENT_PREVIEW_DIR%"
if errorlevel 1 (
  echo ERROR: All 50 tagged MP3s are required to launch.
  echo The website and API were NOT started.
  pause
  exit /b 1
)

echo.
echo First-party AXEZENT music website and API are starting.
echo Local listening URL: http://127.0.0.1:8080/
echo API status URL:      http://127.0.0.1:8080/api/ready
echo.
echo This runs ONLY on this Windows computer.
echo Customers elsewhere cannot open it until you arrange your
echo own public internet connection and HTTPS reverse proxy.
echo No external website host is used.
echo.
start "" "http://127.0.0.1:8080/"
%PYTHON_CMD% server\axezent_site.py --host 127.0.0.1 --port 8080 --preview-dir "%AXEZENT_PREVIEW_DIR%"
echo.
echo AXEZENT website stopped.
pause
endlocal
