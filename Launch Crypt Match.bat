@echo off
title SKULL CRUSH
cd /d "%~dp0"
echo.
echo   ============================
echo     SKULL CRUSH  -  launching
echo   ============================
echo.
set PORT=8761
start "" /min cmd /c "python -m http.server %PORT% --bind 127.0.0.1"
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:%PORT%/index.html"
echo   Game opened in your browser at http://127.0.0.1:%PORT%/index.html
echo   (Keep this window open while playing; close it to stop the server.)
echo.
pause >nul
