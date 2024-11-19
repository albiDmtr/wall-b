import RPi.GPIO as GPIO
import time
from evdev import InputDevice, categorize, ecodes
from openai import OpenAI
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import os
import json
import threading

# GPIO setup for the button
button_pin = 23  # Adjust the pin number as necessary
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

def get_greeting():
    try:
        chat_completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": "You are in a hachathon called Junction. You are supposed to greet people and welcome them to Junction hackathon. Remember, you are extremely sarcastic and say stupid punch line jokes. Your answer should be max one to two sentences long."}
            ]
        )
        greeting = chat_completion.choices[0].message.content.strip()
        return greeting
    except Exception as e:
        print(f"Error getting greeting from ChatGPT: {e}")
        return "Wazzup my homie!"

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

def handle_key_press(key_event):
    global current_voice_id
    if key_event.type == ecodes.EV_KEY:
        key_event = categorize(key_event)
        if key_event.keystate == key_event.key_down:
            if key_event.keycode in ['KEY_A', 'KEY_S']:
                greeting = get_greeting()
                print(f"Greeting generated: {greeting}")
                if key_event.keycode == 'KEY_A':
                    current_voice_id = ELEVENLABS_VOICE_ID_1
                else:
                    current_voice_id = ELEVENLABS_VOICE_ID_2
                play_audio(greeting, current_voice_id)
            elif key_event.keycode == 'KEY_ESC':
                print("Program stopped")
                exit(0)

#def monitor_button():
#    global current_voice_id
#    while True:
#        if GPIO.input(button_pin) == GPIO.LOW:  # Button is pressed
#            print("Button pressed!")  # Debug print to ensure button press is detected
#            greeting = get_greeting()
#            print(f"Greeting generated: {greeting}")
#            current_voice_id = ELEVENLABS_VOICE_ID_1  # Assign a voice ID for button press
#            play_audio(greeting, current_voice_id)
#            while GPIO.input(button_pin) == GPIO.LOW:  # Wait until the button is released
#                time.sleep(0.1)
#        time.sleep(0.1)

def monitor_button():
    global current_voice_id
    while True:
        if GPIO.input(button_pin) == GPIO.LOW:  # Button is pressed
            print("Button pressed!")  # Debug print to ensure button press is detected
            greeting = get_greeting()
            print(f"Greeting generated: {greeting}")
            current_voice_id = ELEVENLABS_VOICE_ID_1  # Assign a voice ID for button press
            play_audio(greeting, current_voice_id)
            while GPIO.input(button_pin) == GPIO.LOW:  # Wait until the button is released
                time.sleep(0.1)
        time.sleep(0.1)

def main():
    keyboard = InputDevice('/dev/input/event8')
    print(f"Listening on {keyboard}")

    # Start the button monitoring thread
    button_thread = threading.Thread(target=monitor_button)
    button_thread.daemon = True  # Ensure the thread closes when the program exits
    button_thread.start()

    try:
        for event in keyboard.read_loop():
            print("lolll")
            handle_key_press(event)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        keyboard.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
