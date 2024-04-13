import speech_recognition as sr

def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)  # Use the Jabra SPEAK 510 USB device index

    with mic as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust this as needed
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()
