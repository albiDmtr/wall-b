from speak.speak import speak

print("Loading model...")
mic_speak = speak()
print("Model loaded...")

mic_speak.speak("Hey, can you hear me?")
