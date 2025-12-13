# Veritasium in a Box

An end-to-end AI-powered content generation pipeline for creating Veritasium-style educational videos.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Multi-Agent   │ -> │   Fine-Tuned    │ -> │    Director     │ -> │   Video Gen     │
│   Research      │    │   Script Gen    │    │    Agent        │    │   (TTS + Vid)   │
│   (Kestra)      │    │   (Llama)       │    │   (Cerebras)    │    │                │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
       ↓                       ↓                       ↓                       ↓
   research_outputs/    research_outputs/    research_outputs/    video_output/
   kestra_output.json   finetuned_script.txt final_5min_script.md generated_tts/
                                                                generated_video/
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- API Keys: `CEREBRAS_API_KEY`, `ELEVENLABS_API_KEY`, `ATLASCLOUD_API_KEY`

### 1. Clone & Setup
```bash
git clone <repo>
cd Veritasium-in-a-Box
cp .env.example .env  # Add your API keys
pip install -r requirements.txt
```

### 2. Start Services
```bash
# Start Kestra (research workflow)
docker-compose up -d

# Or run full pipeline
python3 ai-engine/pipeline.py --topic "The science of why time moves forward"
```

### 3. Generate Video
```bash
cd video_output
python3 video_gen.py --tts elevenlabs
```

## 📁 Project Structure

```
Veritasium-in-a-Box/
├── ai-engine/                 # AI orchestration & director
│   ├── director.py           # Merges research + scripts
│   └── pipeline.py           # Main orchestrator
├── backend/                  # FastAPI backend service
│   ├── main.py              # API endpoints & pipeline orchestration
│   └── requirements.txt     # Backend dependencies
├── kestra/                   # Workflow definitions
│   ├── multi-agent-research.yaml
│   └── generate_kestra_output.py
├── fine_tuned_model/         # Llama fine-tuning
│   └── generate_draft.py
├── frontend/                 # React UI
├── video_output/             # TTS & video generation
│   ├── video_gen.py
│   └── generated_tts/
├── research_outputs/         # Generated content
└── docker-compose.yml
```

## 🔧 Development Commands

### Full Pipeline (Local)
```bash
# Generate research, script, and video
python3 ai-engine/pipeline.py --topic "Quantum entanglement" --debug
```

### Individual Components
```bash
# Just research
cd kestra && python3 generate_kestra_output.py "Your topic"

# Just script generation
cd fine_tuned_model && python3 generate_draft.py --topic "Your topic"

# Just video generation
cd video_output && python3 video_gen.py --tts elevenlabs
```

### Docker Services
```bash
# Start all services
docker-compose up

# Start specific service
docker-compose up kestra
docker-compose up frontend
```

## 🔑 Environment Variables

Create a `.env` file with:
```
CEREBRAS_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
ATLASCLOUD_API_KEY=your_key_here
HUGGINGFACE_TOKEN=your_token_here
```

## 📊 Monitoring & Debugging

### Debug Mode
```bash
python3 ai-engine/pipeline.py --topic "Test topic" --debug
```

### Logs
```bash
# Kestra logs
docker-compose logs kestra

# Check outputs
ls -la research_outputs/
ls -la video_output/generated_tts/
```

## 🚀 Production Deployment

### Docker Swarm
```bash
docker stack deploy -c docker-compose.yml veritasium
```

### API Endpoints
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Kestra UI: `http://localhost:8080`

### Backend API Usage
```bash
# Start content generation
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Quantum physics", "tts_engine": "elevenlabs"}'

# Check status
curl http://localhost:8000/status/{task_id}

# Download generated MP3
curl http://localhost:8000/download/video_output/generated_tts/output.mp3 -o generated_audio.mp3
```

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update this README for API changes
4. Use meaningful commit messages

## 📝 License

MIT License - see LICENSE file for details.