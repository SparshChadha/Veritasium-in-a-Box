#!/usr/bin/env python3
"""
Veritasium Backend API

FastAPI backend that orchestrates the complete content generation pipeline:
1. Research generation (Kestra/local fallback)
2. Script drafting (fine-tuned model)
3. Content merging (Director Agent)
4. TTS generation (ElevenLabs/Edge TTS)
5. Video generation (AtlasCloud)

Endpoints:
- POST /generate: Generate complete video content from topic
- GET /status/{task_id}: Check generation status
- GET /download/{filename}: Download generated files
"""

import asyncio
import subprocess
import os
import json
import uuid
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Veritasium Backend API",
    description="AI-powered educational video content generation",
    version="1.0.0"
)

# Task storage (in production, use Redis/database)
active_tasks: Dict[str, Dict] = {}

class GenerationRequest(BaseModel):
    topic: str
    tts_engine: str = "elevenlabs"
    generate_video: bool = False

class GenerationResponse(BaseModel):
    task_id: str
    status: str
    message: str

def run_research_generation(topic: str) -> bool:
    """Run research generation (Kestra or local fallback)"""
    try:
        # Try Kestra CLI first
        result = subprocess.run([
            "kestra", "flow", "run", "dev.multi-agent-research",
            "-i", f"topic={topic}"
        ], capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            return True

        # Fallback to local script
        result = subprocess.run([
            "python3", "../kestra/generate_kestra_output.py", topic
        ], capture_output=True, text=True, cwd=".", timeout=300)

        return result.returncode == 0
    except Exception as e:
        print(f"Research generation failed: {e}")
        return False

def run_script_generation(topic: str) -> bool:
    """Run script generation using fine-tuned model"""
    try:
        result = subprocess.run([
            "python3", "generate_draft.py", "--topic", topic
        ], capture_output=True, text=True, cwd="../fine_tuned_model", timeout=600)

        return result.returncode == 0
    except Exception as e:
        print(f"Script generation failed: {e}")
        return False

def run_content_merging() -> bool:
    """Run director to merge research and script"""
    try:
        result = subprocess.run([
            "python3", "director.py", "--topic", "Generated Content"
        ], capture_output=True, text=True, cwd="../ai-engine", timeout=300)

        return result.returncode == 0
    except Exception as e:
        print(f"Content merging failed: {e}")
        return False

def run_tts_generation(tts_engine: str) -> bool:
    """Run TTS generation"""
    try:
        result = subprocess.run([
            "python3", "video_gen.py", "--tts", tts_engine
        ], capture_output=True, text=True, cwd="../video_output", timeout=600)

        return result.returncode == 0
    except Exception as e:
        print(f"TTS generation failed: {e}")
        return False

async def run_generation_pipeline(topic: str, tts_engine: str, task_id: str):
    """Run the complete generation pipeline asynchronously"""
    try:
        active_tasks[task_id] = {"status": "running", "step": "Starting pipeline"}

        # Step 1: Research and Script Generation (Parallel)
        active_tasks[task_id] = {"status": "running", "step": "Research & Script Generation"}

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(run_research_generation, topic): "research",
                executor.submit(run_script_generation, topic): "script"
            }

            results = {}
            for future in as_completed(futures):
                task_name = futures[future]
                results[task_name] = future.result()

        if not all(results.values()):
            active_tasks[task_id] = {"status": "failed", "step": "Research/Script generation failed"}
            return

        # Step 2: Content Merging
        active_tasks[task_id] = {"status": "running", "step": "Content Merging"}
        if not run_content_merging():
            active_tasks[task_id] = {"status": "failed", "step": "Content merging failed"}
            return

        # Step 3: TTS Generation
        active_tasks[task_id] = {"status": "running", "step": "TTS Generation"}
        if not run_tts_generation(tts_engine):
            active_tasks[task_id] = {"status": "failed", "step": "TTS generation failed"}
            return

        # Success
        active_tasks[task_id] = {
            "status": "completed",
            "step": "Pipeline completed successfully",
            "files": {
                "research": "research_outputs/kestra_output.json",
                "script": "research_outputs/finetuned_script.txt",
                "final_script": "research_outputs/final_5min_script.md",
                "tts_text": "research_outputs/tts.txt",
                "tts_audio": "video_output/generated_tts/output.mp3"
            }
        }

    except Exception as e:
        active_tasks[task_id] = {"status": "failed", "step": f"Unexpected error: {str(e)}"}

@app.post("/generate", response_model=GenerationResponse)
async def generate_content(request: GenerationRequest, background_tasks: BackgroundTasks):
    """Start content generation pipeline"""
    task_id = str(uuid.uuid4())

    # Start background task
    background_tasks.add_task(run_generation_pipeline, request.topic, request.tts_engine, task_id)

    return GenerationResponse(
        task_id=task_id,
        status="started",
        message=f"Content generation started for topic: {request.topic}"
    )

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    """Check generation status"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    return active_tasks[task_id]

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated files"""
    # Security: only allow specific file types and paths
    allowed_files = [
        "research_outputs/kestra_output.json",
        "research_outputs/finetuned_script.txt",
        "research_outputs/final_5min_script.md",
        "research_outputs/tts.txt",
        "video_output/generated_tts/output.mp3"
    ]

    if filename not in allowed_files:
        raise HTTPException(status_code=403, detail="File not allowed for download")

    file_path = Path(f"../{filename}")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename.split('/')[-1],
        media_type='application/octet-stream'
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
