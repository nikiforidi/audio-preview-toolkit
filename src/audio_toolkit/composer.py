import asyncio
from pathlib import Path
from typing import List, Union
from pydub import AudioSegment

from .analyzer import find_loudest_segment

PathLike = Union[str, Path]


def _process_tracks_sync(
    input_files: List[PathLike],
    target_total_duration_ms: int,
    max_tracks: int,
    crossfade_ms: int,
    fade_in_out_ms: int,
    export_bitrate: str,
    output_path: PathLike
) -> str:
    """Synchronous core logic for audio processing."""
    tracks_to_use = input_files[:max_tracks]
    duration_per_track_ms = target_total_duration_ms // len(tracks_to_use)

    combined_audio: AudioSegment | None = None

    for file_path in tracks_to_use:
        # pydub automatically detects format based on file extension
        audio = AudioSegment.from_file(str(file_path))
        best_segment = find_loudest_segment(audio, duration_per_track_ms)

        if combined_audio is None:
            combined_audio = best_segment
        else:
            combined_audio = combined_audio.append(
                best_segment, crossfade=crossfade_ms)

    if combined_audio is None:
        raise ValueError("No valid audio tracks were processed.")

    # Apply master fade-in and fade-out
    final_audio = combined_audio.fade_in(
        fade_in_out_ms).fade_out(fade_in_out_ms)

    # Export
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    final_audio.export(str(out_path), format="mp3", bitrate=export_bitrate)

    return str(out_path.absolute())


async def generate_smart_preview(
    input_files: List[PathLike],
    output_path: PathLike,
    target_total_duration_ms: int = 30000,
    max_tracks: int = 4,
    crossfade_ms: int = 500,
    fade_in_out_ms: int = 500,
    export_bitrate: str = "192k"
) -> str:
    """
    Generates a smart audio preview from a list of local audio files.

    This is an async wrapper that runs the CPU-intensive pydub operations 
    in a thread pool to avoid blocking the asyncio event loop.
    """
    if not input_files:
        raise ValueError("At least one input file is required")

    return await asyncio.to_thread(
        _process_tracks_sync,
        input_files,
        target_total_duration_ms,
        max_tracks,
        crossfade_ms,
        fade_in_out_ms,
        export_bitrate,
        output_path
    )
