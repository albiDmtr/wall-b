from evdev import InputDevice, categorize, ecodes
from openai import OpenAI
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import os
import json

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

def main():
    keyboard = InputDevice('/dev/input/event0')

    print(f"Listening on {keyboard.path}")
    try:
        while True:
            for fd in r:
                for event in keyboard.read():
                    handle_key_press(event)
            if conversation_active and not stop_listening.is_set():
                threading.Thread(target=listen_to_speech).start()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        keyboard.close()

def main():
    keyboard = InputDevice('/dev/input/event0')

    print(f"Listening on {keyboard}")
    try:
        for event in keyboard.read_loop():
            handle_key_press(event)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        keyboard.close()

if __name__ == "__main__":
    main()