# 🎵 audio-preview-toolkit

[![PyPI version](https://img.shields.io/pypi/v/audio-preview-toolkit.svg)](https://pypi.org/project/audio-preview-toolkit/)
[![Python Version](https://img.shields.io/pypi/pyversions/audio-preview-toolkit.svg)](https://pypi.org/project/audio-preview-toolkit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A pure, source-agnostic Python toolkit for generating **smart, loudness-optimized audio previews**.

Instead of blindly cutting the first N seconds of a track, `audio-preview-toolkit` uses a sliding-window RMS (Root Mean Square) analysis to dynamically find the loudest, most energetic parts of your audio. It then seamlessly trims, crossfades, and concatenates multiple tracks into a single, professional-sounding preview (perfect for vinyl releases, podcasts, or music streaming cards).

## ✨ Features

- 🧠 **Smart Loudness Analysis**: Automatically skips silent intros/outros and finds the "meat" of the track using RMS amplitude analysis.
- ⚖️ **Dynamic Duration Splitting**: Automatically divides the target preview duration evenly across the provided tracks (e.g., 4 tracks = 7.5s each for a 30s preview).
- 🎛️ **Professional Audio Polishing**: Applies seamless crossfades between segments and master fade-in/fade-out effects.
- 🚀 **Async-First Design**: The core composer runs CPU-intensive `pydub` operations in a thread pool, ensuring it never blocks your `asyncio` event loop.
- 🔌 **Source-Agnostic**: Zero network dependencies. It operates purely on local file paths, making it incredibly easy to test, mock, and integrate into any architecture (FastAPI, ARQ, Celery, CLI, etc.).

## ⚠️ Prerequisites

This library relies on [`pydub`](https://github.com/jiaaro/pydub), which requires **`ffmpeg`** to be installed on your host system or inside your Docker container to read, process, and export audio files.

**Ubuntu/Debian:**
```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
