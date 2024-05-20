#GPIO can be only used with Raspberry Pi

from evdev import InputDevice, categorize, ecodes
#import RPi.GPIO as GPIO
from openai import OpenAI
from evdev import InputDevice, categorize, ecodes
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import speech_recognition as sr
import time
import os
import json

# GPIO setup
#left_wheel_pin = 17
#right_wheel_pin = 22
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(left_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.setup(right_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)

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

def listen_to_speech(recognizer, microphone):
    #with microphone as source:
    #    print("Listening for speech...")
    #    audio = recognizer.listen(source)
    #try:
    #    text = recognizer.recognize_google(audio)
    #    print(f"Recognized speech: {text}")
    #    return text
    #except sr.UnknownValueError:
    #    print("Speech recognition could not understand audio")
    #    return None
    #except sr.RequestError as e:
    #    print(f"Could not request results from Google Speech Recognition service; {e}")
    #    return None
    #change text2 to respond_to_speech
   
    # Simulate recognized speech for testing
    print("Simulating speech recognition...")
    time.sleep(2)  # Simulate delay for speech recognition
    simulated_text = "Tell me more about the Build It hackathon."
    print(f"Recognized speech: {simulated_text}")
    return simulated_text


def respond_to_speech(simulated_text):
    try:
        chat_completion2 = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "The assistant is helpful, extremely sarcastic, and engages in conversation about Build It hackathons that are hosted every 2 to 3 weeks at Startup Sauna. Your answer is max 10 words."},
                {"role": "user", "content": simulated_text}
            ]
        )
        response = chat_completion2.choices[0].message.content.strip()
        return response
    except Exception as e:
        print(f"Error responding to speech with ChatGPT: {e}")
        return "Sorry, I couldn't understand that."

def handle_key_press(key_event):
    global conversation_active, current_voice_id
    if key_event.type == ecodes.EV_KEY:
        key_event = categorize(key_event)
        if key_event.keystate == key_event.key_down:
            if key_event.keycode in ['KEY_A', 'KEY_S']:
                # Start or restart the conversation with the appropriate greeting
                conversation_active = False  # Reset conversation
                greeting = get_greeting()
                print(f"Greeting generated: {greeting}")
                if key_event.keycode == 'KEY_A':
                    current_voice_id = ELEVENLABS_VOICE_ID_1
                else:
                    current_voice_id = ELEVENLABS_VOICE_ID_2
                play_audio(greeting, current_voice_id)
                conversation_active = True
            elif key_event.keycode == 'KEY_ESC':
                print("Program stopped")
                exit(0)
            elif key_event.keycode == 'KEY_RIGHT':
                #GPIO.output(right_wheel_pin, GPIO.LOW)
                print("Left wheel is ON")
            elif key_event.keycode == 'KEY_LEFT':
                #GPIO.output(left_wheel_pin, GPIO.LOW)
                print("Right wheel is ON")
            elif key_event.keycode == 'KEY_UP':
                #GPIO.output(left_wheel_pin, GPIO.LOW)
                #GPIO.output(right_wheel_pin, GPIO.LOW)
                print("Both wheels are ON")    

def main():
    keyboard = InputDevice('/dev/input/event0')

    print(f"Listening on {keyboard}")
    try:
        for event in keyboard.read_loop():
            handle_key_press(event)
            if conversation_active:
                speech_text = listen_to_speech(recognizer, microphone)
                if speech_text:
                    response = respond_to_speech(speech_text)
                    play_audio(response, current_voice_id)
                    time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        keyboard.close()

if __name__ == "__main__":
    main()