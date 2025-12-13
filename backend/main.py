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
import shutil
import time
import logging
from datetime import datetime
from typing import Dict, Optional, Any, Tuple
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Veritasium Backend API",
    description="AI-powered educational video content generation",
    version="1.0.0"
)

# CORS (dev-friendly; tighten for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


def _project_root() -> Path:
    # Prefer explicit root (useful in Docker), else infer from file location:
    # backend/main.py -> backend/ -> project root
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return Path(__file__).resolve().parent.parent


def ensure_dirs(root: Path):
    """Ensure output directories exist"""
    dirs = [
        root / "research_outputs",
        root / "video_output" / "generated_tts",
        root / "video_output" / "generated_video",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def _init_task(task_id: str, topic: str, tts_engine: str, generate_video: bool) -> Dict[str, Any]:
    return {
        "task_id": task_id,
        "topic": topic,
        "tts_engine": tts_engine,
        "generate_video": generate_video,
        "status": "running",
        "current_step": "starting",
        "steps": {
            "research": {"status": "pending", "label": "Kestra research → kestra_output.json", "log": ""},
            "draft": {"status": "pending", "label": "Fine-tuned model → finetuned_script.txt", "log": ""},
            "director": {"status": "pending", "label": "Director merge → final_5min_script.md + tts.txt", "log": ""},
            "tts": {"status": "pending", "label": "TTS → output.mp3", "log": ""},
            "video": {"status": "pending", "label": "Video generation (WaveSpeed) → .mp4", "log": ""},
        },
        "files": {},
        "error": None,
        "updated_at": datetime.now().isoformat(),
    }


def _set_step(task_id: str, step_key: str, status: str, current_step: Optional[str] = None, log: Optional[str] = ""):
    task = active_tasks.get(task_id)
    if not task:
        return
    # FIXED: Use setdefault to ensure step exists and update in-place
    step = task["steps"].setdefault(step_key, {"status": "pending", "label": step_key, "log": ""})
    step["status"] = status
    if log:
        step["log"] = log[-1000:]  # Trim for UI
    if current_step is not None:
        task["current_step"] = current_step
    task["updated_at"] = datetime.now().isoformat()


def _set_failed(task_id: str, message: str):
    # FIXED: Task-level only (no "final" step)
    task = active_tasks.get(task_id)
    if not task:
        return
    task["status"] = "failed"
    task["current_step"] = "failed"
    task["error"] = message
    task["updated_at"] = datetime.now().isoformat()
    logger.error(f"Task {task_id} failed: {message}")


def _parse_final_output(stdout: str) -> Optional[str]:
    # video_gen.py prints: "🎉 Final Output: <path>"
    for line in reversed(stdout.splitlines()):
        if "Final Output:" in line:
            return line.split("Final Output:", 1)[1].strip()
    return None

def run_research_generation(topic: str, retries: int = 3) -> Tuple[bool, str]:
    """Run research generation (Kestra or local fallback)"""
    root = _project_root()
    ensure_dirs(root)
    env = os.environ.copy()

    for attempt in range(retries):
        try:
            kestra_bin = shutil.which("kestra")
            if kestra_bin:
                logger.info(f"Research attempt {attempt+1}: Kestra CLI")
                result = subprocess.run(
                    [kestra_bin, "flow", "run", "dev.multi-agent-research", "-i", f"topic={topic}"],
                    capture_output=True,
                    text=True,
                    timeout=180,
                    cwd=str(root),
                    env=env,
                )
                if result.returncode == 0:
                    return True, ""
                log = result.stderr[:500]
            else:
                logger.info(f"Research attempt {attempt+1}: Falling back to local script...")
            # FIXED: Use --output-dir for correct path
            cmd = [
                "python3", str(root / "kestra" / "generate_kestra_output.py"),
                topic, "--output", "kestra_output.json", "--output-dir", str(root / "research_outputs")
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(root / "kestra"),
                timeout=180,
                env=env,
            )
            output_file = root / "research_outputs" / "kestra_output.json"
            if result.returncode == 0 and output_file.exists():
                logger.info(f"Research success: {output_file}")
                return True, ""
            log = result.stderr[:500] or "No output file created"
        except subprocess.TimeoutExpired:
            log = "Timeout"
        except Exception as e:
            log = str(e)
        logger.error(f"Research attempt {attempt+1} failed: {log}")
        if attempt < retries - 1:
            time.sleep(5)
    return False, log


def run_script_generation(topic: str) -> Tuple[bool, str]:
    """Run script generation using fine-tuned model"""
    root = _project_root()
    ensure_dirs(root)
    env = os.environ.copy()
    cmd = ["python3", "generate_draft.py", "--topic", topic]
    logger.info(f"Draft gen: {' '.join(cmd)}")
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(root / "fine_tuned_model"), timeout=300, env=env
    )
    script_file = root / "research_outputs" / "finetuned_script.txt"
    if result.returncode == 0 and script_file.exists():
        logger.info(f"Draft success: {script_file}")
        return True, ""
    log = result.stderr[:500] or "No output file"
    logger.error(f"Draft failed: {log}")
    return False, log


def run_content_merging(topic: str) -> Tuple[bool, str]:
    """Run director to merge research and script"""
    root = _project_root()
    ensure_dirs(root)
    env = os.environ.copy()
    cmd = ["python3", "director.py", "--topic", topic]
    logger.info(f"Director: {' '.join(cmd)}")
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(root / "ai-engine"), timeout=300, env=env
    )
    script_file = root / "research_outputs" / "final_5min_script.md"
    tts_file = root / "research_outputs" / "tts.txt"
    if result.returncode == 0 and script_file.exists() and tts_file.exists():
        logger.info("Director success")
        return True, ""
    log = result.stderr[:500] or "Missing outputs"
    logger.error(f"Director failed: {log}")
    return False, log


def run_tts_and_video_generation(tts_engine: str, generate_video: bool) -> Dict[str, Any]:
    """Run TTS (and optionally video) via video_gen.py. Returns output paths."""
    root = _project_root()
    ensure_dirs(root)
    env = os.environ.copy()
    if not generate_video:
        # video_gen.py skips video generation if WAVESPEED_API_KEY is missing
        env.pop("WAVESPEED_API_KEY", None)

    cmd = ["python3", "video_gen.py", "--tts", tts_engine]
    logger.info(f"TTS/Video: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(root / "video_output"),
        timeout=600,
        env=env,
    )

    final_output = _parse_final_output(result.stdout)
    # audio file is stable in video_gen.py
    audio_path = str(root / "video_output" / "generated_tts" / "output.mp3")
    video_path: Optional[str] = final_output if final_output and final_output.endswith(".mp4") else None

    ok = bool(result.returncode == 0 and Path(audio_path).exists())
    log = result.stderr[:1000] if not ok else ""
    logger.info(f"TTS/Video ok: {ok}, video_path: {video_path}")

    return {
        "ok": ok,
        "audio_path": audio_path if Path(audio_path).exists() else None,
        "video_path": video_path,
        "stdout": result.stdout[-2000:],
        "stderr": result.stderr[-2000:],
        "log": log,
    }


async def run_generation_pipeline(topic: str, tts_engine: str, generate_video: bool, task_id: str):
    """Run the complete generation pipeline asynchronously"""
    try:
        active_tasks[task_id] = _init_task(task_id, topic, tts_engine, generate_video)
        logger.info(f"Pipeline {task_id}: Started {topic}")

        # Step 1: Research and Script Generation (Parallel)
        _set_step(task_id, "research", "running", current_step="research")
        _set_step(task_id, "draft", "running")

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(run_research_generation, topic): "research",
                executor.submit(run_script_generation, topic): "draft"
            }

            for future in as_completed(futures):
                task_name = futures[future]
                success, log_msg = future.result()
                step_key = task_name
                status = "completed" if success else "failed"
                _set_step(task_id, step_key, status, log=log_msg)
                if not success:
                    _set_failed(task_id, f"{step_key.capitalize()} failed: {log_msg}")
                    return

        # Step 2: Content Merging
        _set_step(task_id, "director", "running", current_step="director")
        success, log_msg = run_content_merging(topic)
        status = "completed" if success else "failed"
        _set_step(task_id, "director", status, log=log_msg)
        if not success:
            _set_failed(task_id, f"Director failed: {log_msg}")
            return

        # Step 3: TTS (and optionally video)
        _set_step(task_id, "tts", "running", current_step="tts")
        if generate_video:
            _set_step(task_id, "video", "running")
        else:
            _set_step(task_id, "video", "skipped")

        out = run_tts_and_video_generation(tts_engine, generate_video)
        tts_status = "completed" if out.get("ok") else "failed"
        tts_log = out.get("log", "")
        _set_step(task_id, "tts", tts_status, log=tts_log)
        if generate_video:
            v_status = "completed" if out.get("video_path") else "failed"
            v_log = out.get("log", "")
            _set_step(task_id, "video", v_status, log=v_log)
        if not out.get("ok"):
            _set_failed(task_id, f"TTS/video failed: {tts_log}")
            return

        # Success
        root = _project_root()
        files = {
            "research": "research_outputs/kestra_output.json",
            "script": "research_outputs/finetuned_script.txt",
            "final_script": "research_outputs/final_5min_script.md",
            "tts_text": "research_outputs/tts.txt",
            "tts_audio": "video_output/generated_tts/output.mp3",
        }
        video_rel: Optional[str] = None
        if out.get("video_path"):
            # Try to convert to project-relative path
            try:
                video_rel = str(Path(str(out["video_path"])).resolve().relative_to(root))
            except Exception:
                video_rel = str(out.get("video_path"))
            files["video"] = video_rel

        task = active_tasks.get(task_id, {})
        task["status"] = "completed"
        task["current_step"] = "completed"
        task["files"] = files
        task["updated_at"] = datetime.now().isoformat()
        logger.info(f"Pipeline {task_id}: Completed")

    except Exception as e:
        logger.error(f"Pipeline {task_id}: Unexpected error: {str(e)}")
        _set_failed(task_id, f"Unexpected error: {str(e)}")


@app.post("/generate", response_model=GenerationResponse)
async def generate_content(request: GenerationRequest, background_tasks: BackgroundTasks):
    """Start content generation pipeline"""
    task_id = str(uuid.uuid4())

    # Start background task
    background_tasks.add_task(run_generation_pipeline, request.topic, request.tts_engine, request.generate_video, task_id)

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


@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    """Download generated files"""
    # Security: only allow specific file types and paths
    allowed_files = [
        "research_outputs/kestra_output.json",
        "research_outputs/finetuned_script.txt",
        "research_outputs/final_5min_script.md",
        "research_outputs/tts.txt",
        "video_output/generated_tts/output.mp3"
    ]

    # Allow generated videos (pattern) if present
    is_generated_video = (
        file_path.startswith("video_output/generated_video/generated_video_")
        and file_path.endswith(".mp4")
    )

    if file_path not in allowed_files and not is_generated_video:
        raise HTTPException(status_code=403, detail="File not allowed for download")

    root = _project_root()
    disk_path = root / file_path
    if not disk_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=disk_path,
        filename=file_path.split('/')[-1],
        media_type='application/octet-stream'
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/test-pipeline")
async def test_pipeline(request: GenerationRequest):
    """Test endpoint (sync for debugging; remove for prod)"""
    task_id = str(uuid.uuid4())
    await run_generation_pipeline(request.topic, request.tts_engine, request.generate_video, task_id)
    return active_tasks.get(task_id, {"error": "Task not found"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)