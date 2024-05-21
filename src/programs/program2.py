from evdev import InputDevice, categorize, ecodes
from openai import OpenAI
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import speech_recognition as sr
import time
import os
import json
import threading
import select

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

OPENAI_API_KEY = config.get('OPENAI_API_KEY')
ELEVENLABS_API_KEY = config.get('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID_1 = 'lxNNOU4CuwcLA6DP9pL4'
ELEVENLABS_VOICE_ID_2 = 'dfry7bk7VysVw6GgZmvx'

# Initialize the OpenAI and ElevenLabs clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

conversation_active = False
current_voice_id = None
stop_listening = threading.Event()
listening_thread = None
lock = threading.Lock()

def get_greeting():
    try:
        chat_completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": "You are an extremely sarcastic AI who likes to say mean and fly jokes. Your task is to relentlessly market a hackathon called Build It to people who are in front of you and really trying to force them to scan the qr code below. Generate only 2 sentences or less."}
            ]
        )
        greeting = chat_completion.choices[0].message.content.strip()
        return greeting
    except Exception as e:
        print(f"Error getting greeting from ChatGPT: {e}")
        return "Wazzup my homie. Join Build It hackathon, scan the QR code below!"

def play_audio(text, voice_id):
    try:
        audio = elevenlabs_client.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2"
        )
        play(audio)
    except Exception as e:
        print(f"An error occurred during audio generation or playback: {e}")

def listen_to_speech():
    global conversation_active, listening_thread
    while conversation_active:
        with lock:  # Ensure no other thread can access the microphone
            with microphone as source:
                print("Listening for speech...")
                recognizer.adjust_for_ambient_noise(source)
                print("Adjusting for ambient noise")
                audio = recognizer.listen(source)
                print("Created audio = recognizer.listen(source)")
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized speech: {text}")
            if len(text.split()) >= 3:  # Check if the recognized speech has at least 3 words
                response = respond_to_speech(text)
                play_audio(response, current_voice_id)
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        finally:
            if not stop_listening.is_set():
                print("Continuing to listen...")
                # Restart the thread to continue listening
                listening_thread = threading.Thread(target=listen_to_speech)
                listening_thread.start()
                break
            else:
                conversation_active = False
                stop_listening.clear()

def respond_to_speech(text):
    try:
        chat_completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "The assistant is helpful, extremely sarcastic, and engages in conversation about Build It hackathons that are hosted every 2 to 3 weeks at Startup Sauna. Generate only 2 sentences or less."},
                {"role": "user", "content": text}
            ]
        )
        response = chat_completion.choices[0].message.content.strip()
        return response
    except Exception as e:
        print(f"Error responding to speech with ChatGPT: {e}")
        return "Sorry, I couldn't understand that."

def handle_key_press(key_event):
    global conversation_active, current_voice_id, stop_listening, listening_thread
    if key_event.type == ecodes.EV_KEY:
        key_event = categorize(key_event)
        if key_event.keystate == key_event.key_down:
            if key_event.keycode in ['KEY_A', 'KEY_S']:
                print(f"Key {key_event.keycode} pressed, starting conversation...")
                if stop_listening.is_set():
                    stop_listening.clear()
                conversation_active = False  # Reset conversation
                greeting = get_greeting()
                print(f"Greeting generated: {greeting}")
                if key_event.keycode == 'KEY_A':
                    current_voice_id = ELEVENLABS_VOICE_ID_1
                else:
                    current_voice_id = ELEVENLABS_VOICE_ID_2
                play_audio(greeting, current_voice_id)
                conversation_active = True
                if listening_thread and listening_thread.is_alive():
                    stop_listening.set()
                    listening_thread.join()
                listening_thread = threading.Thread(target=listen_to_speech)
                listening_thread.start()
            elif key_event.keycode == 'KEY_ESC':
                print("Program stopped")
                conversation_active = False
                stop_listening.set()
                if listening_thread and listening_thread.is_alive():
                    listening_thread.join()
                exit(0)

def main():
    keyboard = InputDevice('/dev/input/event0')

    print(f"Listening on {keyboard.path}")
    try:
        while True:
            r, _, _ = select.select([keyboard.fd], [], [], 0.1)
            for fd in r:
                for event in keyboard.read():
                    handle_key_press(event)
            if conversation_active and not stop_listening.is_set():
                stop_listening.set()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        keyboard.close()

if __name__ == "__main__":
    main()