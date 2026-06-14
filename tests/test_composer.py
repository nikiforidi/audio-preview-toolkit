import pytest
import tempfile
from pathlib import Path
from pydub import AudioSegment
from pydub.generators import Sine
from audio_toolkit.composer import generate_smart_preview


@pytest.fixture
def temp_audio_files():
    """Generate temporary MP3 files for testing."""
    files = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        for i in range(3):
            # Create a 5-second audio file with a distinct tone
            audio = Sine(440 + (i * 100)
                         ).to_audio_segment(duration=5000, volume=-6.0)
            file_path = Path(tmp_dir) / f"track_{i}.mp3"
            audio.export(str(file_path), format="mp3")
            files.append(str(file_path))
        yield files


@pytest.mark.asyncio
async def test_generate_smart_preview_single_track(temp_audio_files):
    """Test preview generation with a single track."""
    output_path = "test_output_single.mp3"

    try:
        # Request 2 seconds from a 5-second track
        result_path = await generate_smart_preview(
            input_files=[temp_audio_files[0]],
            output_path=output_path,
            target_total_duration_ms=2000,
            max_tracks=1,
            crossfade_ms=0,  # No crossfade for single track
            fade_in_out_ms=0
        )

        assert Path(result_path).exists()
        assert Path(result_path).is_absolute()

        # Verify duration (allow 100ms margin for MP3 encoding overhead)
        final_audio = AudioSegment.from_file(result_path)
        assert 1900 <= len(final_audio) <= 2100

    finally:
        if Path(output_path).exists():
            Path(output_path).unlink()


@pytest.mark.asyncio
async def test_generate_smart_preview_multiple_tracks_with_crossfade(temp_audio_files):
    """Test preview generation with multiple tracks and crossfading."""
    output_path = "test_output_multi.mp3"

    try:
        # Request 6 seconds total from 3 tracks (2 seconds each)
        result_path = await generate_smart_preview(
            input_files=temp_audio_files,
            output_path=output_path,
            target_total_duration_ms=6000,
            max_tracks=3,
            crossfade_ms=500,
            fade_in_out_ms=0
        )

        assert Path(result_path).exists()

        final_audio = AudioSegment.from_file(result_path)

        # With 3 tracks of 2000ms and 500ms crossfade between them:
        # Track 1: 2000ms
        # Track 2: adds 1500ms (2000 - 500 overlap)
        # Track 3: adds 1500ms (2000 - 500 overlap)
        # Total expected: 5000ms (allow margin for encoding)
        assert 4800 <= len(final_audio) <= 5200

    finally:
        if Path(output_path).exists():
            Path(output_path).unlink()


@pytest.mark.asyncio
async def test_generate_smart_preview_empty_input():
    """Should raise ValueError if no input files are provided."""
    with pytest.raises(ValueError, match="At least one input file is required"):
        await generate_smart_preview(
            input_files=[],
            output_path="fail.mp3"
        )
