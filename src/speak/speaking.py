import subprocess
from chatgpt_utils import get_greeting

def speak_text(text):
    """Uses espeak to convert text to speech."""
    print(f"Speaking: {text}")  # Print what will be spoken
    subprocess.run(['espeak', text])

# Get the greeting text
greeting_text = get_greeting()

# Speak the greeting
speak_text(greeting_text)