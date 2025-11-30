# Step-by-Step Guide to Run the Application

## Prerequisites
1. Python 3.8+ (✅ You have this)
2. Node.js 18+ (⚠️ Need to install)

## Installation Steps

### 1. Install Node.js
- Download from: https://nodejs.org/
- Install the LTS version
- Restart your terminal after installation

### 2. Install Frontend Dependencies
Open a terminal and run:
```bash
cd c:\Users\sabar\OneDrive\Desktop\Voice\frontend
npm install
```

This will install all React dependencies (takes 2-3 minutes).

## Running the Application

### Method 1: Using Batch Scripts (Easiest)

#### Start Backend:
Double-click: `start-backend.bat`
OR run in terminal:
```bash
cd c:\Users\sabar\OneDrive\Desktop\Voice
start-backend.bat
```

#### Start Frontend:
Double-click: `start-frontend.bat`
OR run in terminal:
```bash
cd c:\Users\sabar\OneDrive\Desktop\Voice
start-frontend.bat
```

### Method 2: Manual Commands

#### Terminal 1 - Backend:
```bash
cd c:\Users\sabar\OneDrive\Desktop\Voice\backend
python app.py
```

Wait for: "Uvicorn running on http://0.0.0.0:8000"

#### Terminal 2 - Frontend:
```bash
cd c:\Users\sabar\OneDrive\Desktop\Voice\frontend
npm run dev
```

Wait for: "Local: http://localhost:3000"

## Access the Application

1. Backend API: http://localhost:8000
2. API Docs: http://localhost:8000/docs
3. Frontend App: http://localhost:3000 ← **Open this in your browser**

## Stopping the Application

Press `Ctrl+C` in each terminal window to stop the servers.

## Troubleshooting

### "node not found"
- Install Node.js from https://nodejs.org/
- Restart your terminal

### "npm not found"
- Node.js installation includes npm
- Restart your terminal

### "Port already in use"
- Close other instances
- Or change port in backend/app.py

### Backend errors
- Ensure you're in the Voice directory
- Check that all Python dependencies are installed

## What You'll See

### Backend Terminal:
```
========================================
🚀 Starting Indic Speech-to-English Translation API Server
========================================
📍 Server: http://localhost:8000
📖 API Docs: http://localhost:8000/docs
========================================
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend Terminal:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Browser:
Beautiful web interface with:
- Language selector
- Record/Upload tabs
- Microphone recording
- File upload
- Results display

## Quick Test

1. Open http://localhost:3000
2. Select "Hindi" language
3. Click "Record Audio"
4. Click the microphone button
5. Speak in Hindi
6. Click stop
7. Click "Translate"
8. See your transcription and English translation!

## Need Help?

- Check GETTING_STARTED.md for detailed guide
- Check WEB_APP_README.md for API documentation
- Ensure both backend and frontend are running
- Check browser console (F12) for errors
