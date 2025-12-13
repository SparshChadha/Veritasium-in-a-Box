# Veritasium Backend API

FastAPI backend for orchestrating the complete Veritasium content generation pipeline.

## Features

- **Asynchronous Processing**: Non-blocking content generation
- **Parallel Execution**: Research and script generation run simultaneously
- **Status Tracking**: Real-time progress monitoring
- **File Downloads**: Secure access to generated content
- **Health Monitoring**: System health checks

## API Endpoints

### POST `/generate`
Start content generation pipeline.

**Request Body:**
```json
{
  "topic": "The science of why time moves forward",
  "tts_engine": "elevenlabs",
  "generate_video": false
}
```

**Response:**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "started",
  "message": "Content generation started for topic: The science of why time moves forward"
}
```

### GET `/status/{task_id}`
Check generation status.

**Response:**
```json
{
  "status": "running",
  "step": "Content Merging",
  "files": {
    "research": "research_outputs/kestra_output.json",
    "script": "research_outputs/finetuned_script.txt",
    "final_script": "research_outputs/final_5min_script.md",
    "tts_text": "research_outputs/tts.txt",
    "tts_audio": "video_output/generated_tts/output.mp3"
  }
}
```

### GET `/download/{filename}`
Download generated files.

**Allowed files:**
- `research_outputs/kestra_output.json`
- `research_outputs/finetuned_script.txt`
- `research_outputs/final_5min_script.md`
- `research_outputs/tts.txt`
- `video_output/generated_tts/output.mp3`

### GET `/health`
Health check endpoint.

## Pipeline Flow

1. **Research Generation** (Parallel with Script Gen)
   - Kestra CLI → `research_outputs/kestra_output.json`
   - Fallback: Local script if Kestra unavailable

2. **Script Generation** (Parallel with Research)
   - Fine-tuned model → `research_outputs/finetuned_script.txt`

3. **Content Merging**
   - Director Agent combines research + script → `research_outputs/tts.txt`

4. **TTS Generation**
   - ElevenLabs/Edge TTS → `video_output/generated_tts/output.mp3`

## Usage

### Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Production
```bash
docker build -t veritasium-backend .
docker run -p 8000:8000 veritasium-backend
```

### With Docker Compose
```bash
docker-compose up backend
```

## Environment Variables

```bash
CEREBRAS_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
ATLASCLOUD_API_KEY=your_key
```

## Frontend Integration

The backend is designed to work with the React frontend. The frontend can:

1. POST to `/generate` to start generation
2. Poll `/status/{task_id}` for progress updates
3. Download the final MP3 via `/download/video_output/generated_tts/output.mp3`
