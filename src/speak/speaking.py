import subprocess
import time
from chatgpt_utils import get_greeting

def speak_text(text):
    """Uses espeak to convert text to speech with an Indian accent."""
    print(f"Speaking: {text}")  # Print what will be spoken
    # Specify the voice for Indian English accent
    subprocess.run(['espeak', '-v', 'en+f4', text])

def continuously_speak():
    while True:
        greeting_text = get_greeting()
        speak_text(greeting_text)
        time.sleep(7)  # Wait for 7 seconds before the next call

# Start the continuous speaking process
continuously_speak()

#openai bot with memory:
#https://www.youtube.com/watch?v=cHjlperESbg