import RPi.GPIO as GPIO
import time
import subprocess

# Set up the GPIO pin
button_pin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable internal pull-up resistor

try:
    while True:
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.LOW:
            subprocess.run(["mpg321", "public\stop.mp3"])
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()     
