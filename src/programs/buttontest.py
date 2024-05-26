import RPi.GPIO as GPIO
import time

# Set up the GPIO pin
button_pin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable internal pull-up resistor

try:
    while True:
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.HIGH:  # Button pressed (connected to GND)
            print("Button Pressed")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
