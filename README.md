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
```

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Docker:**
```dockerfile
RUN apt-get update && apt-get install -y ffmpeg
```

## 📦 Installation

Install the latest version from PyPI:

```bash
pip install audio-preview-toolkit
```

## 🚀 Quick Start

### 1. Generate a Smart Preview (Async)
The primary use case. Pass a list of local audio file paths, and get back a perfectly mixed, 30-second MP3 preview.

```python
import asyncio
from audio_toolkit import generate_smart_preview

async def main():
    # Provide a list of local audio files
    track_paths = [
        "path/to/track_01.mp3",
        "path/to/track_02.mp3",
        "path/to/track_03.mp3",
        "path/to/track_04.mp3",
    ]

    print("🎵 Generating smart preview...")

    output_path = await generate_smart_preview(
        input_files=track_paths,
        output_path="vinyl_release_preview.mp3",
        target_total_duration_ms=30000,  # 30 seconds total
        max_tracks=4,                    # Use up to 4 tracks
        crossfade_ms=500,                # 500ms overlap between tracks
        fade_in_out_ms=500,              # Master fade in/out
        export_bitrate="192k"
    )

    print(f"✅ Preview saved to: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Find the Loudest Segment (Sync)
If you want to build your own custom audio processing pipeline, you can use the underlying analyzer directly.

```python
from pydub import AudioSegment
from audio_toolkit import find_loudest_segment

# Load an audio file
audio = AudioSegment.from_file("my_long_track.mp3")

# Find the loudest 10-second window
best_part = find_loudest_segment(audio, target_duration_ms=10000)

# Export just that loud part
best_part.export("loudest_10_seconds.mp3", format="mp3")
```

## 🛠️ API Reference

### `generate_smart_preview(...)`
An async wrapper that runs the audio processing in a background thread.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_files` | `List[str \| Path]` | *Required* | List of local paths to audio files. |
| `output_path` | `str \| Path` | *Required* | Where to save the final generated MP3. |
| `target_total_duration_ms` | `int` | `30000` | Target length of the final preview in milliseconds. |
| `max_tracks` | `int` | `4` | Maximum number of tracks to include from the input list. |
| `crossfade_ms` | `int` | `500` | Overlap in milliseconds between concatenated segments. |
| `fade_in_out_ms` | `int` | `500` | Master fade-in and fade-out duration at the start/end. |
| `export_bitrate` | `str` | `"192k"` | MP3 export bitrate. |

### `find_loudest_segment(audio, target_duration_ms)`
A synchronous function that analyzes a `pydub.AudioSegment` and returns the contiguous window with the highest RMS amplitude.

---

## 🧪 Development & Testing

If you want to contribute or run the test suite locally, clone the repository and set up the development environment:

```bash
# Clone the repo
git clone https://github.com/nikiforidi/audio-preview-toolkit.git
cd audio-preview-toolkit

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install core + dev dependencies (pytest, ruff, pre-commit)
pip install -r requirements-dev.txt

# Run the test suite
pytest tests/ -v
```

### Using the Dev Container
This repository includes a `.devcontainer` configuration. If you use VS Code, simply click **"Reopen in Container"** to get a fully pre-configured environment with Python 3.11, `ffmpeg`, and `git` pre-installed.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
