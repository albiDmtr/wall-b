import time
from elevenlabs import play
from elevenlabs.client import ElevenLabs

# Set your ElevenLabs API key and voice ID directly in the script
ELEVENLABS_API_KEY = ''
ELEVENLABS_VOICE_ID = ''

# Initialize the ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def play_audio(text):
    try:
        # Generate the audio from text using ElevenLabs API
        audio = client.generate(
            text=text,
            voice=ELEVENLABS_VOICE_ID,
            model="eleven_multilingual_v2"
        )

        # Play the audio
        play(audio)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("Enter text to be narrated by David Attenborough (type 'exit' to quit):")

    while True:
        # Read text input from the terminal
        user_input = input("> ")

        if user_input.lower() == "exit":
            break

        print("🎙️ David says:")
        print(user_input)

        # Generate and play the audio
        play_audio(user_input)

        # Wait for a bit before the next input
        time.sleep(1)

if __name__ == "__main__":
    main()
