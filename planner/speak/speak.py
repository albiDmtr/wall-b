import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice
from pathlib import Path

class speak:
    def __init__(self):
        base_dir = Path(__file__).parent.absolute()
        speech_model = (base_dir / 'models' / 'en_US-joe-medium.onnx').as_posix()
        self._voice = PiperVoice.load(speech_model)

    def speak(self, text):
        stream = sd.OutputStream(samplerate=self._voice.config.sample_rate, channels=1, dtype='int16')
        stream.start()

        for audio_bytes in self._voice.synthesize_stream_raw(text):
            int_data = np.frombuffer(audio_bytes, dtype=np.int16)
            stream.write(int_data)

        stream.stop()
        stream.close()