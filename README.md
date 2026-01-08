# Whisper FastAPI Transcription Backend

A production-ready FastAPI backend for OpenAI Whisper speech-to-text transcription, optimized for deployment on Render's free tier.

## Features

- **FastAPI + Uvicorn**: Modern, fast HTTP server
- **OpenAI Whisper**: State-of-the-art speech recognition
- **Tiny Model**: CPU-friendly model for fast startup and low resource usage
- **File Upload**: Accept `.mp3`, `.wav`, `.m4a` audio files
- **Error Handling**: JSON error responses with meaningful messages
- **Temp File Cleanup**: Automatic cleanup of uploaded files after processing
- **Health Check**: `/` endpoint for monitoring
- **Render Ready**: Pre-configured for Render deployment

## API Endpoints

### Health Check
```
GET /
```
Returns service status and model info.

**Response:**
```json
{
  "status": "healthy",
  "service": "Whisper Transcription API",
  "model": "tiny"
}
```

### Transcribe Audio
```
POST /transcribe
```
Transcribe an audio file to text.

**Request:**
- Content-Type: `multipart/form-data`
- Parameter: `file` (type: File)
- Supported formats: `.mp3`, `.wav`, `.m4a`

**Response (Success - 200):**
```json
{
  "text": "transcribed text from audio file"
}
```

**Response (Error - 400):**
```json
{
  "detail": "Unsupported file type: .xyz. Supported types: .mp3, .wav, .m4a"
}
```

**Response (Error - 500):**
```json
{
  "detail": "Transcription failed: <error details>"
}
```

## Local Development

### Prerequisites
- Python 3.9+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd whisper-fastapi-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   python main.py
   ```
   Server runs on `http://localhost:8000`

5. **Access interactive API docs**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Render Deployment

### Step 1: Prepare Repository
1. Push your code to GitHub
2. Ensure you have `main.py` and `requirements.txt` in the root directory

### Step 2: Create Render Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in the configuration:
   - **Name**: `whisper-api` (or your preferred name)
   - **Environment**: `Python 3.9`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free tier (sufficient for demo/testing)

### Step 3: Deploy
1. Click "Create Web Service"
2. Render will automatically build and deploy
3. Copy the service URL (e.g., `https://whisper-api.onrender.com`)
4. Monitor logs in the Render dashboard

### Step 4: Test Deployment
```bash
# Health check
curl https://whisper-api.onrender.com/

# Test transcription (replace with your audio file)
curl -X POST https://whisper-api.onrender.com/transcribe \
  -F "file=@/path/to/audio.mp3"
```

## Postman Testing

### 1. Health Check
- **Method**: GET
- **URL**: `http://localhost:8000/`
- **Expected Response** (200):
  ```json
  {
    "status": "healthy",
    "service": "Whisper Transcription API",
    "model": "tiny"
  }
  ```

### 2. Transcribe Audio
- **Method**: POST
- **URL**: `http://localhost:8000/transcribe`
- **Body**:
  - Select "form-data"
  - Key: `file`
  - Type: **File** (click the file icon)
  - Value: Select your audio file (.mp3, .wav, or .m4a)

- **Example Response** (200):
  ```json
  {
    "text": "Hello, how are you today?"
  }
  ```

### Testing with cURL
```bash
# Health check
curl -X GET http://localhost:8000/

# Transcribe audio file
curl -X POST http://localhost:8000/transcribe \
  -F "file=@path/to/your/audio.mp3"

# Pretty print response
curl -X POST http://localhost:8000/transcribe \
  -F "file=@path/to/your/audio.mp3" | jq
```

## Performance Notes

- **Model**: Uses Whisper "tiny" (74M parameters)
- **Language**: Configured for English ("en")
- **Startup Time**: ~10-15 seconds (first request may be slower as model loads)
- **Processing Time**: Depends on audio length (typically 2-5x real-time for short clips)
- **Memory**: ~1GB peak (comfortable on Render free tier with 512MB RAM for Python runtime)
- **CPU**: Fully CPU-based (GPU not available on Render free tier)

## Model Options

The "tiny" model is recommended for Render's free tier. If you need better accuracy, you can switch to:

- `tiny`: 39M params, fastest (default)
- `base`: 74M params, balanced (recommended for better accuracy)
- `small`: 244M params, slower
- `medium`: 769M params, slower yet
- `large`: 1550M params, slowest

To change, edit `main.py` line 23:
```python
model = whisper.load_model("base")  # Change "tiny" to another option
```

## Troubleshooting

### Service won't start
- Check Render logs for errors
- Ensure `requirements.txt` is in the root directory
- Verify Python version is 3.9+

### Transcription takes too long
- Render free tier CPU is limited
- For production use, upgrade to paid tier
- Consider using larger audio files (overhead is amortized)

### File upload fails
- Ensure file format is .mp3, .wav, or .m4a
- Check file size (very large files may timeout on free tier)
- Verify Content-Type is multipart/form-data

### Out of memory errors
- Switch to "tiny" model if using larger model
- Reduce concurrent requests
- Upgrade to paid Render plan for more memory

## Environment Variables

- `PORT`: Server port (default: 8000, auto-set by Render to $PORT)

No additional configuration needed for local development or Render deployment.

## Project Structure

```
whisper-fastapi-backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## License

MIT - Feel free to use this project for commercial and personal use.

## Support

For issues or questions:
1. Check Render deployment logs
2. Review the API documentation at `/docs`
3. Test locally first before deploying to Render