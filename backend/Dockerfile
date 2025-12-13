# Backend Dockerfile for Veritasium API (monorepo build)
# IMPORTANT: Build context should be the repo root.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROJECT_ROOT=/app

WORKDIR /app

# System deps needed by some Python packages + healthcheck curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps (backend + pipeline scripts)
COPY backend/requirements.txt /app/backend/requirements.txt
COPY kestra/requirements.txt /app/kestra/requirements.txt
COPY ai-engine/requirements.txt /app/ai-engine/requirements.txt

RUN pip install --no-cache-dir -r /app/backend/requirements.txt \
  && pip install --no-cache-dir -r /app/kestra/requirements.txt \
  && pip install --no-cache-dir -r /app/ai-engine/requirements.txt

# Copy the code the backend orchestrates (baked into image for deployment)
COPY backend/ /app/backend/
COPY kestra/ /app/kestra/
COPY fine_tuned_model/ /app/fine_tuned_model/
COPY ai-engine/ /app/ai-engine/
COPY video_output/ /app/video_output/

WORKDIR /app/backend

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
