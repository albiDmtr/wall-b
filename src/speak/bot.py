import imageio
import numpy as np
from PIL import Image
import numpy as np
from chatgpt_utils import get_greeting  # Make sure this points to your correct file
from gtts import gTTS
import pygame
import tempfile
import speech_recognition as sr
from openai import OpenAI
import json
import os
import time

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.json')

# Read the config.json file
with open(config_path, 'r') as f:
    config = json.load(f)

# Access the OPENAI_API_KEY
OPENAI_API_KEY = config.get('OPENAI_API_KEY')

def initialize_pygame_mixer():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)

def play_speech(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(f"{fp.name}.mp3")
        pygame.mixer.music.load(f"{fp.name}.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def listen_and_recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for speech...")
        audio = r.listen(source, timeout=5, phrase_time_limit=8)
    try:
        text = r.recognize_google(audio)
        print(f"Recognized speech: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error; {e}")
        return None
        
def get_chatgpt_response(text):
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        response = chat_completion.choices[0].message.content.strip()
        return response
    except Exception as e:
        print(f"Error: {e}")
        return "Ship product like a motherfucker"
        
def capture_frame(reader):
    """Capture a frame from the video source and convert it to grayscale."""
    frame = reader.get_next_data()  # Capture frame
    frame = Image.fromarray(frame)  # Convert to PIL Image
    frame = frame.convert('L')  # Convert to grayscale
    return np.array(frame)  # Convert back to numpy array for analysis

def detect_motion(frame1, frame2, threshold=50000):
    """Detect motion by comparing two frames."""
    # Compute the absolute difference between the two frames
    diff = np.abs(frame1.astype("int") - frame2.astype("int"))
    # Check if the sum of the absolute differences is greater than the threshold
    motion_detected = np.sum(diff) > threshold
    return motion_detected    

def detect_motion_and_interact():
    reader = imageio.get_reader('/dev/video1') #/dev/media3
    last_frame = capture_frame(reader)

    greeting = get_greeting()
    print("Greeting:", greeting)
    play_speech(greeting)

    current_frame = capture_frame(reader)
    motion_detected = False

    while True:
        if motion_detected:
            print("Motion detected!")
            user_speech = listen_and_recognize()
            if user_speech:
                response = get_chatgpt_response(user_speech)
                play_speech(response)
        else:
            print("No motion detected.")
        
        time.sleep(1)
        last_frame = current_frame
        current_frame = capture_frame(reader)
        motion_detected = detect_motion(last_frame, current_frame)


def conversation_loop():
    user_speech = listen_and_recognize()
    while user_speech:
        response = get_chatgpt_response(user_speech)
        play_speech(response)
        user_speech = listen_and_recognize()

if __name__ == "__main__":
    initialize_pygame_mixer()
    detect_motion_and_interact()