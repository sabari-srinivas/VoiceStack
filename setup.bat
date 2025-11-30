@echo off
echo ========================================
echo   Indic Speech Translator
echo   Complete Setup
echo ========================================
echo.

echo [1/3] Installing Python dependencies...
cd /d "%~dp0"
pip install -r requirements.txt
cd backend
pip install -r requirements.txt
cd ..

echo.
echo [2/3] Installing Node.js dependencies...
cd frontend
call npm install
cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Run: start-backend.bat
echo   2. Run: start-frontend.bat
echo   3. Open: http://localhost:3000
echo.
echo ========================================

pause
