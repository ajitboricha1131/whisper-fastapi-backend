import os
import tempfile
import whisper
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Whisper Transcription API", version="1.0.0")

# Load Whisper model at startup
model = None

@app.on_event("startup")
async def load_model():
    """Load Whisper model at startup"""
    global model
    try:
        logger.info("Loading Whisper model (tiny)...")
        model = whisper.load_model("tiny")
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Whisper Transcription API",
        "model": "tiny"
    }


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """
    Transcribe audio file using Whisper
    
    Accepts: .mp3, .wav, .m4a files
    Returns: {"text": "transcribed text"}
    """
    
    # Validate file type
    allowed_types = {".mp3", ".wav", ".m4a"}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Supported types: {', '.join(allowed_types)}"
        )
    
    temp_file = None
    try:
        # Create temporary file with original extension
        with tempfile.NamedTemporaryFile(
            suffix=file_ext,
            delete=False
        ) as tmp:
            temp_file = tmp.name
            # Write uploaded file to temp location
            contents = await file.read()
            tmp.write(contents)
        
        logger.info(f"Processing file: {file.filename}")
        
        # Transcribe using Whisper
        result = model.transcribe(temp_file, language="en")
        transcribed_text = result.get("text", "").strip()
        
        logger.info(f"Transcription completed. Length: {len(transcribed_text)} chars")
        
        return JSONResponse(
            status_code=200,
            content={"text": transcribed_text}
        )
    
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
                logger.info("Temporary file cleaned up")
            except Exception as e:
                logger.warning(f"Failed to delete temp file: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False
    )
