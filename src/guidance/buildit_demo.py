import RPi.GPIO as GPIO
import time

left_wheel_pin = 17  # GPIO pin you are using
right_wheel_pin = 22
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme

GPIO.setup(left_wheel_pin, GPIO.OUT)
GPIO.setup(right_wheel_pin, GPIO.OUT)
time.sleep(1)  # Sleep for 1 second

GPIO.output(left_wheel_pin, True)
while True:
    # circle

    # left turn
    time.sleep(0.5)

    # straight
    GPIO.output(right_wheel_pin, True)
    time.sleep(0.5)
    GPIO.output(right_wheel_pin, False)



GPIO.cleanup()