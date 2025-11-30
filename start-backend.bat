@echo off
echo ========================================
echo   Indic Speech Translator - Backend
echo ========================================
echo.

cd /d "%~dp0backend"

echo Installing backend dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Starting FastAPI server...
echo ========================================
echo.
echo API Server: http://localhost:8000
echo API Docs:   http://localhost:8000/docs
echo ReDoc:      http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
