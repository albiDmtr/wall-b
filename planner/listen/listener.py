import os
import sys
import numpy as np
import time
from contextlib import contextmanager

@contextmanager
def suppress_audio_errors():
    """Low-level stderr suppression that works on Raspberry Pi"""
    # Save original stderr
    original_stderr = os.dup(2)
    
    # Redirect stderr to /dev/null
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 2)
    os.close(devnull)
    
    try:
        yield
    finally:
        # Restore original stderr
        os.dup2(original_stderr, 2)
        os.close(original_stderr)

with suppress_audio_errors():
    import speech_recognition as sr
    from faster_whisper import WhisperModel

class listener:
    def __init__(self):
            self._model = WhisperModel('base.en', device="cpu", compute_type="int8")

    def listen(self, seconds_max, stop_on_silence=True):
        with suppress_audio_errors():
            r = sr.Recognizer()
        
            with sr.Microphone(sample_rate=16000) as source:
                print("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                print("Listening...")
                try:
                    audio = r.listen(source, timeout=seconds_max, phrase_time_limit=(3 if stop_on_silence else seconds_max))
                except sr.WaitTimeoutError:
                    audio = None

        if audio is not None:
            audio_np = np.frombuffer(audio.get_raw_data(), dtype=np.int16).astype(np.float32) / 32768.0

            start_time = time.time()
            segments, _ = self._model.transcribe(audio_np)
            segments = list(segments)
            transcription = " ".join([segment.text for segment in segments])
            end_time = time.time()
            print(f"Transcription of {(len(audio_np) / 16000):.2f} seconds took {end_time - start_time:.2f} seconds.")
        else:
            transcription = ""

        print("Transcription:")
        print(transcription)

        return transcription
