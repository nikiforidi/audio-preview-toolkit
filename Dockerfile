# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout for clean logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies:
# - ffmpeg: REQUIRED by pydub to read, process, and export audio files
# - git: REQUIRED by pre-commit to manage and run hooks
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements first to leverage Docker layer caching
COPY requirements-dev.txt .

# Install Python dependencies (installs the toolkit in editable mode + dev tools)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy the rest of the application code
COPY . .

# Optional: Automatically install the git hooks when the container builds
RUN pre-commit install || true

# Default command to keep the dev container running
CMD ["sleep", "infinity"]