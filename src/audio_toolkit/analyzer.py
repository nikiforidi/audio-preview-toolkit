from pydub import AudioSegment


def find_loudest_segment(audio: AudioSegment, target_duration_ms: int) -> AudioSegment:
    """
    Finds the loudest contiguous segment of the target duration using RMS analysis.
    If the audio is shorter than the target duration, it returns the entire audio.
    """
    if len(audio) <= target_duration_ms:
        return audio

    step_ms = 1000  # Slide the window in 1-second increments
    max_rms = -1
    best_start = 0

    for i in range(0, len(audio) - target_duration_ms + 1, step_ms):
        chunk = audio[i: i + target_duration_ms]
        rms = chunk.rms
        if rms > max_rms:
            max_rms = rms
            best_start = i

    return audio[best_start: best_start + target_duration_ms]
