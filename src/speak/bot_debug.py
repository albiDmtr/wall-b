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
    print("Initializing Pygame Mixer...")
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)
    print("Pygame Mixer initialized.")

def play_speech(text):
    print(f"Playing speech: {text[:50]}...")  # Show beginning of text to be played
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(f"{fp.name}.mp3")
        pygame.mixer.music.load(f"{fp.name}.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    print("Finished playing speech.")

def listen_and_recognize():
    print("Entering listen_and_recognize function.")
    r = sr.Recognizer()
    device_index = 1  # Adjust as needed
    with sr.Microphone(device_index=device_index) as source:
        print("Listening for speech...")
        r.adjust_for_ambient_noise(source)  # this line is optional, to improve recognition accuracy
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        except Exception as e:
            print(f"Error during listening: {e}")
            return None
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
    print(f"Getting ChatGPT response for: {text}")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        response = chat_completion.choices[0].message.content.strip()
        print(f"Received ChatGPT response: {response[:50]}...")  # Show beginning of response
        return response
    except Exception as e:
        print(f"Error: {e}")
        return "There was an error getting a response. Please try again."

def interact():
    print("Robot started")

    try:
        greeting = get_greeting()
        print("Greeting:", greeting)
        play_speech(greeting)

        while True:
            print("Listening...")
            user_speech = listen_and_recognize()
            if user_speech:
                response = get_chatgpt_response(user_speech)
                play_speech(response)
            else:
                print("No speech detected.")
    except Exception as e:
        print(f"Unexpected error in interact function: {e}")

if __name__ == "__main__":
    try:
        initialize_pygame_mixer()
        interact()
    except Exception as e:
        print(f"Fatal error in main: {e}")