@echo off
echo ========================================
echo   Quick Setup - Frontend Dependencies
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Checking Node.js installation...
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js not found!
    echo.
    echo Please install Node.js from: https://nodejs.org/
    echo After installation, restart your computer.
    echo.
    pause
    exit /b 1
)

echo Node.js found!
node --version
npm --version
echo.

echo Installing frontend dependencies...
echo This will take 2-3 minutes...
echo.

call npm install

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Frontend is ready!
    echo ========================================
    echo.
    echo You can now run:
    echo   - start-backend.bat
    echo   - start-frontend.bat
    echo.
) else (
    echo.
    echo ========================================
    echo   ERROR during installation
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause
