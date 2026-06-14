import pytest
from pydub import AudioSegment
from pydub.generators import Sine, Silence
from audio_toolkit.analyzer import find_loudest_segment


def test_find_loudest_segment_shorter_than_target():
    """If audio is shorter than target, it should return the whole audio."""
    # Create 2 seconds of audio
    audio = AudioSegment.silent(duration=2000)

    # Request 5 seconds
    result = find_loudest_segment(audio, target_duration_ms=5000)

    assert len(result) == 2000
    assert result == audio


def test_find_loudest_segment_finds_loud_burst():
    """Should correctly identify the window with the highest RMS amplitude."""
    # Create 10 seconds of total audio
    # 0-3s: Silent
    # 3-6s: Loud (Sine wave at 440Hz)
    # 6-10s: Silent
    silent_1 = AudioSegment.silent(duration=3000)
    loud_burst = Sine(440).to_audio_segment(
        duration=3000, volume=-3.0)  # -3 dBFS (loud)
    silent_2 = AudioSegment.silent(duration=4000)

    audio = silent_1 + loud_burst + silent_2

    # Request a 3-second segment
    target_ms = 3000
    result = find_loudest_segment(audio, target_duration_ms=target_ms)

    # The result should be exactly the loud burst
    assert len(result) == target_ms
    assert result.rms > loud_burst.rms * 0.9  # Allow tiny float margin
    assert result.rms > 1000  # Silent audio has RMS near 0, loud is much higher


def test_find_loudest_segment_exact_match():
    """If audio length equals target, return the whole audio."""
    audio = AudioSegment.silent(duration=5000)
    result = find_loudest_segment(audio, target_duration_ms=5000)
    assert len(result) == 5000
