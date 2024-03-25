import cv2
import numpy as np
from chatgpt_utils import get_greeting  # Make sure this points to your correct file
from gtts import gTTS
import pygame
import tempfile
import speech_recognition as sr
from openai import OpenAI
import json
import os

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
        
def recalibrate_baseline(cap, frames_to_skip=30):
    for _ in range(frames_to_skip):
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
    return gray        

def find_working_camera():
    index = 0
    num_of_cameras = 10  # Adjust this value based on your expectation
    while index < num_of_cameras:
        cap = cv2.VideoCapture(index)
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', index)
        else:
            return cap
        index += 1
    return None

def detect_motion_and_interact():
    cap = find_working_camera()
    if cap is None:
        raise Exception("No working camera found")  
    prev_gray = recalibrate_baseline(cap)

    motion_detected = False

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not motion_detected:
            for contour in contours:
                if cv2.contourArea(contour) < 5000:  # Adjust this value as needed
                    continue
                print("Motion detected.")
                motion_detected = True
                greeting = get_greeting()
                print("Greeting:", greeting)
                play_speech(greeting)
                break

        if motion_detected:
            user_speech = listen_and_recognize()
            if user_speech:
                response = get_chatgpt_response(user_speech)
                play_speech(response)
            else:
                # Recalibrate baseline frame to avoid immediate retriggering
                print("Waiting for new motion...")
                prev_gray = recalibrate_baseline(cap)
                motion_detected = False

        if cv2.waitKey(10) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def conversation_loop():
    user_speech = listen_and_recognize()
    while user_speech:
        response = get_chatgpt_response(user_speech)
        play_speech(response)
        user_speech = listen_and_recognize()

if __name__ == "__main__":
    initialize_pygame_mixer()
    detect_motion_and_interact()