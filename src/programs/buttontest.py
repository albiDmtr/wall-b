import simpleaudio as sa
import RPi.GPIO as GPIO
import time

# Load the WAV file (use raw string or double backslashes)
wave_obj = sa.WaveObject.from_wave_file(r"public\stop.wav")

# GPIO setup
button_pin = 16  # Adjust the pin number as necessary
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.LOW:
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Wait until sound has finished playing
            while GPIO.input(button_pin) == GPIO.LOW:
                time.sleep(0.1)  # Wait until the button is released
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()