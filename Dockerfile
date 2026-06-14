FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install ffmpeg (for pydub) and git (for pre-commit)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /workspace

# 🔑 CRITICAL: Copy the dev requirements file (not requirements.txt)
COPY requirements-dev.txt .

# Install dependencies (this installs the toolkit in editable mode + dev tools)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy the rest of the repository code
COPY . .

# Automatically install git hooks
RUN pre-commit install || true

# Keep the container running for VS Code to attach to
CMD ["sleep", "infinity"]
