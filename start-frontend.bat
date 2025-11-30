@echo off
echo ========================================
echo   Indic Speech Translator - Frontend
echo ========================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
    echo.
)

echo ========================================
echo Starting React development server...
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

call npm run dev

pause
