import os
import numpy as np
import speech_recognition as sr
import whisper
from datetime import datetime, timedelta
from queue import Queue
from time import sleep

class listener():
    def __init__(self):
        self._data_queue = Queue()
        self._recorder = sr.Recognizer()
        self._recorder.energy_threshold = 1000
        self._recorder.dynamic_energy_threshold = False

        # might cause issues on some platforms, need to test
        self._source = sr.Microphone(sample_rate=16000)
        
        self._audio_model = whisper.load_model('base.en')

    def listen(self, record_timeout=2, phrase_timeout=3):
        transcription = ['']

        with self._source:
            self._recorder.adjust_for_ambient_noise(self._source)

        def record_callback(_, audio:sr.AudioData) -> None:
            # Grab the raw bytes and push it into the thread safe queue.
            data = audio.get_raw_data()
            self._data_queue.put(data)

        self._recorder.listen_in_background(self._source, record_callback, phrase_time_limit=record_timeout)

        print("Model loaded.\n")

        phrase_time = None
        phrase_bytes = bytes()
        while True:
            try:
                now = datetime.now()
                # pull raw recorded audio from the queue.
                if not self._data_queue.empty():
                    phrase_complete = False
                    # if enough time has passed between recordings, consider the phrase complete.
                    # clear the current working audio buffer to start over with the new data.
                    if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                        phrase_bytes = bytes()
                        phrase_complete = True
                    # this is the last time we received new audio data from the queue.
                    phrase_time = now
                    
                    # combine audio data from queue
                    audio_data = b''.join(self._data_queue.queue)
                    self._data_queue.queue.clear()

                    # add the new audio data to the accumulated data for this phrase
                    phrase_bytes += audio_data

                    # convert in-ram buffer to something the model can use directly without needing a temp file.
                    # convert data from 16 bit wide integers to floating point with a width of 32 bits.
                    # clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                    audio_np = np.frombuffer(phrase_bytes, dtype=np.int16).astype(np.float32) / 32768.0

                    # read the transcription.
                    start_time = datetime.now()
                    result = self._audio_model.transcribe(audio_np, fp16=False)
                    end_time = datetime.now()
                    print(f"Transcription took {end_time - start_time} seconds.")
                    print(f"Transcription: {result['text']}")

                    text = result['text'].strip()

                    # if we detected a pause between recordings, add a new item to our transcription.
                    # otherwise edit the existing one.
                    if phrase_complete:
                        transcription.append(text)
                    else:
                        transcription[-1] = text
                else:
                    sleep(0.25)
            except KeyboardInterrupt:
                break

        return " ".join(transcription)

        