@echo off
setlocal
cd /d "%~dp0"
echo ============================================
echo     AXEZENT BEATS FOR SALE - PLAY MODE
echo ============================================
echo.
echo Starting private tagged-MP3 player at http://127.0.0.1:8080
echo 50 Play buttons activate only if the private preview folder contains each file.
echo To keep the MP3s out of GitHub, put them in a SIBLING folder:
echo AXEZENT_PRIVATE_TAGGED_PREVIEWS
echo.
echo No download or payment capability will be enabled.
echo.
where py >nul 2>nul
if %errorlevel% equ 0 (
    start "" "http://127.0.0.1:8080"
    py server\axezent_site.py --host 127.0.0.1 --port 8080
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        start "" "http://127.0.0.1:8080"
        python server\axezent_site.py --host 127.0.0.1 --port 8080
    ) else (
        echo Python 3 was not found.
        echo Install it from https://www.python.org/downloads/
        pause
    )
)
endlocal
