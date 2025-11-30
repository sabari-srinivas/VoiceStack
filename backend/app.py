"""
FastAPI Backend for Indic Speech-to-English Translation
Provides REST API endpoints for audio processing
"""

# Fix Windows encoding
import sys
import os
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import logging

# ... (imports remain the same)

# ... (rest of the file until main block)

# Add parent directory to path to import pipeline
sys.path.append(str(Path(__file__).parent.parent))

from pipeline import IndicSpeechToEnglishPipeline, list_supported_languages
from config import SUPPORTED_LANGUAGES
from gemini_service import GeminiRefiner

# Gemini API configuration
GEMINI_API_KEY = ""
gemini_refiner = None

try:
    gemini_refiner = GeminiRefiner(GEMINI_API_KEY)
except Exception as e:
    logger.warning(f"Failed to initialize Gemini API: {str(e)}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Indic Speech-to-English Translation API",
    description="Convert Indic language speech to English text",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global pipeline cache
pipelines = {}

def get_pipeline(language_code: str):
    """Get or create pipeline for a language"""
    if language_code not in pipelines:
        logger.info(f"Loading pipeline for language: {language_code}")
        pipelines[language_code] = IndicSpeechToEnglishPipeline(
            language_code=language_code,
            device='cpu'  # Use CPU for compatibility
        )
    return pipelines[language_code]


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Indic Speech-to-English Translation API",
        "version": "1.0.0",
        "endpoints": {
            "GET /languages": "List supported languages",
            "POST /translate": "Translate audio to English",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "loaded_pipelines": list(pipelines.keys())
    }


@app.get("/languages")
async def get_languages():
    """Get list of supported languages"""
    languages = []
    for code, info in SUPPORTED_LANGUAGES.items():
        languages.append({
            "code": code,
            "name": info["name"],
            "script": info["script"],
            "flores_code": info["flores_code"]
        })
    
    return {
        "total": len(languages),
        "languages": languages
    }


@app.post("/translate")
async def translate_audio(
    audio: UploadFile = File(...),
    language: str = Form(...)
):
    """
    Translate audio file to English
    
    Parameters:
    - audio: Audio file (WAV, MP3, FLAC, OGG, etc.)
    - language: Language code (hi, ta, te, ml, kn, mr, gu, bn, or, pa)
    
    Returns:
    - JSON with transcription and translation
    """
    
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}. Supported: {list(SUPPORTED_LANGUAGES.keys())}"
        )
    
    # Create temporary file for audio
    temp_dir = tempfile.mkdtemp()
    temp_audio_path = None
    
    try:
        # Save uploaded file
        file_extension = Path(audio.filename).suffix or '.wav'
        temp_audio_path = os.path.join(temp_dir, f"audio{file_extension}")
        
        with open(temp_audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        logger.info(f"Processing audio file: {audio.filename} ({language})")
        
        # Get or create pipeline
        pipeline = get_pipeline(language)
        
        # Process audio
        result = pipeline.process(
            audio_path=temp_audio_path,
            output_dir=None,  # Don't save to disk
            save_intermediate=False,
            verbose=False
        )
        
        # Refine translation with Gemini
        refined_prompt = None
        if gemini_refiner:
            try:
                logger.info("Refining translation with Gemini...")
                refined_prompt = gemini_refiner.refine_to_prototype_prompt(result["english_text"])
                logger.info("Gemini refinement successful!")
            except Exception as e:
                logger.warning(f"Gemini refinement failed: {str(e)}")
                refined_prompt = None
        
        # Prepare response
        response = {
            "success": True,
            "language": {
                "code": language,
                "name": result["language"]["name"],
                "script": result["language"]["script"]
            },
            "transcription": result["indic_text"],
            "translation": result["english_text"],
            "refined_prompt": refined_prompt,  # Add refined prompt
            "processing_time": result["processing_time"],
            "timestamp": result["timestamp"],
            "filename": audio.filename
        }
        
        logger.info(f"Successfully processed: {audio.filename}")
        return JSONResponse(content=response)
    
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio: {str(e)}"
        )
    
    finally:
        # Cleanup temporary files
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


@app.post("/translate-batch")
async def translate_batch(
    files: list[UploadFile] = File(...),
    language: str = Form(...)
):
    """
    Translate multiple audio files
    
    Parameters:
    - files: List of audio files
    - language: Language code
    
    Returns:
    - JSON with results for each file
    """
    
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}"
        )
    
    results = []
    
    for audio_file in files:
        try:
            result = await translate_audio(audio_file, language)
            results.append(result)
        except Exception as e:
            results.append({
                "success": False,
                "filename": audio_file.filename,
                "error": str(e)
            })
    
    return {
        "total": len(files),
        "successful": sum(1 for r in results if r.get("success", False)),
        "results": results
    }


if __name__ == "__main__":
    # Run server
    print("=" * 70)
    print("Starting Indic Speech-to-English Translation API Server")
    print("=" * 70)
    print(f"Server: http://localhost:8000")
    print(f"API Docs: http://localhost:8000/docs")
    print(f"ReDoc: http://localhost:8000/redoc")
    print("=" * 70)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
