# Indic Speech Translator - Web Application

Complete web application with React frontend and FastAPI backend.

## 🚀 Quick Start

### Backend Setup

1. **Install backend dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Start the backend server**:
```bash
python app.py
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Install Node.js dependencies**:
```bash
cd frontend
npm install
```

2. **Start the development server**:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## 📁 Project Structure

```
Voice/
├── backend/
│   ├── app.py                 # FastAPI server
│   └── requirements.txt       # Backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AudioRecorder.jsx    # Microphone recording
│   │   │   ├── FileUpload.jsx       # File upload
│   │   │   ├── LanguageSelector.jsx # Language picker
│   │   │   └── ResultDisplay.jsx    # Results display
│   │   ├── App.jsx            # Main app component
│   │   ├── api.js             # API client
│   │   └── main.jsx           # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── pipeline.py                # Core pipeline
├── asr_module.py              # ASR module
├── nmt_module.py              # NMT module
└── config.py                  # Configuration
```

## 🎯 Features

### Frontend
- ✅ **Microphone Recording**: Record audio directly in browser
- ✅ **File Upload**: Drag-and-drop or browse for files
- ✅ **10 Languages**: Select from all supported Indic languages
- ✅ **Real-time Processing**: Live status updates
- ✅ **Beautiful UI**: Modern, responsive design
- ✅ **Copy & Download**: Easy result sharing

### Backend
- ✅ **REST API**: FastAPI with automatic docs
- ✅ **CORS Enabled**: Works with any frontend
- ✅ **File Validation**: Type and size checks
- ✅ **Error Handling**: Comprehensive error messages
- ✅ **Health Checks**: Monitor server status

## 🔧 API Endpoints

### GET /languages
Get list of supported languages

**Response**:
```json
{
  "total": 10,
  "languages": [
    {
      "code": "hi",
      "name": "Hindi",
      "script": "Devanagari",
      "flores_code": "hin_Deva"
    },
    ...
  ]
}
```

### POST /translate
Translate audio to English

**Parameters**:
- `audio`: Audio file (multipart/form-data)
- `language`: Language code (form field)

**Response**:
```json
{
  "success": true,
  "language": {
    "code": "hi",
    "name": "Hindi",
    "script": "Devanagari"
  },
  "transcription": "मूल हिंदी पाठ",
  "translation": "Original Hindi text",
  "processing_time": {
    "asr": 2.34,
    "nmt": 0.56,
    "total": 2.90
  },
  "timestamp": "2025-11-29T10:00:00",
  "filename": "audio.wav"
}
```

### GET /health
Health check endpoint

## 🎨 UI Components

### AudioRecorder
- Microphone access
- Recording timer
- Audio playback
- Waveform visualization

### FileUpload
- Drag-and-drop support
- File type validation
- Size limits (50MB)
- Preview before upload

### LanguageSelector
- Grid layout
- Visual language cards
- Active state indication

### ResultDisplay
- Transcription display
- Translation display
- Processing stats
- Copy to clipboard
- Download results

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Backend Development
```bash
cd backend
python app.py    # Start server with auto-reload
```

## 📝 Environment Variables

### Backend
No environment variables required. All configuration is in `config.py`.

### Frontend
API URL is configured in `src/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000'
```

## 🚀 Production Deployment

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
# Serve the 'dist' folder with any static server
```

## 🔍 Troubleshooting

### Backend Issues

**"Module not found"**
```bash
# Ensure you're in the Voice directory
cd c:\Users\sabar\OneDrive\Desktop\Voice
pip install -r requirements.txt
```

**"Port already in use"**
- Change port in `app.py`: `uvicorn.run(app, port=8001)`

### Frontend Issues

**"npm not found"**
- Install Node.js from https://nodejs.org/

**"Cannot connect to backend"**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app.py`

**Microphone not working**
- Grant microphone permissions in browser
- Use HTTPS in production (required for mic access)

## 📊 Performance

### Backend Processing Times (CPU)
- 10s audio: ~20-30s
- 30s audio: ~40-60s
- 1min audio: ~80-120s

### Frontend
- Initial load: < 2s
- Recording: Real-time
- Upload: Depends on file size

## 🌟 Tips

1. **Use Chrome/Edge** for best microphone support
2. **Grant permissions** when prompted for mic access
3. **Keep audio short** (< 1 minute) for faster processing
4. **Use WAV format** for best quality
5. **Check backend logs** for debugging

## 📖 Additional Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev/
- Vite Docs: https://vitejs.dev/
- AI4Bharat: https://ai4bharat.org/

## 🎉 You're Ready!

1. Start backend: `cd backend && python app.py`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: `http://localhost:3000`
4. Select language and start recording!

---

**Enjoy translating! 🌏**
