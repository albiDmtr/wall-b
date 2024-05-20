from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import speech_recognition as sr
import os
import json

app = Flask(__name__)

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

OPENAI_API_KEY = config.get('OPENAI_API_KEY')
ELEVENLABS_API_KEY = config.get('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID_1 = 'lxNNOU4CuwcLA6DP9pL4'
ELEVENLABS_VOICE_ID_2 = 'dfry7bk7VysVw6GgZmvx'

openai_client = OpenAI(api_key=OPENAI_API_KEY)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    voice_id = request.json['voice_id']
    greeting = get_greeting()
    play_audio(greeting, voice_id)
    return jsonify({'message': greeting})

@app.route('/respond', methods=['POST'])
def respond():
    voice_id = request.json['voice_id']
    simulated_text = request.json['text']
    response = respond_to_speech(simulated_text)
    play_audio(response, voice_id)
    return jsonify({'message': response})

def get_greeting():
    try:
        chat_completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": "You are an extremely sarcastic AI who likes to say mean and fly jokes. Your task is to relentlessly market a hackathon called Build It to people who are in front of you and really trying to force them to scan the qr code below. Generate only 12 words or less."}
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
        audio_data = b''.join(audio)
        with open('audio.mp3', 'wb') as f:
            f.write(audio_data)
        # Play the audio using aplay or any other command-line audio player available on Raspberry Pi
        os.system('mpg321 audio.mp3')  # You can use mpg321, aplay, or any other audio player
    except Exception as e:
        print(f"An error occurred during audio generation or playback: {e}")

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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
