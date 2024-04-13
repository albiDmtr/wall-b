import RPi.GPIO as GPIO
import time

left_wheel_pin = 17  # GPIO pin you are using
right_wheel_pin = 22
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme

while True:
    GPIO.setup(left_wheel_pin, GPIO.OUT)
    GPIO.output(left_wheel_pin, True)
    time.sleep(2)
    GPIO.output(left_wheel_pin, False)

    GPIO.setup(right_wheel_pin, GPIO.OUT)
    GPIO.output(right_wheel_pin, True)
    time.sleep(2)
    GPIO.output(right_wheel_pin, False)
    time.sleep(2)

GPIO.cleanup()