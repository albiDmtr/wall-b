import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setwarnings(False)

# Define GPIO pins for Motor 1 and Motor 2
Motor1 = 17  # Pin connected to the first motor
Motor2 = 22  # Pin connected to the second motor

# Set up the motor pins:
GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)

# Function to turn on a motor
def motor_on(pin):
    GPIO.output(pin, True)

# Function to turn off a motor
def motor_off(pin):
    GPIO.output(pin, False)

try:
    while True:
        # Turn Motor 1 on
        motor_on(Motor1)
        time.sleep(2)

        # Turn Motor 1 off
        motor_off(Motor1)
        time.sleep(2)

        # Turn Motor 2 on
        motor_on(Motor2)
        time.sleep(2)

        # Turn Motor 2 off
        motor_off(Motor2)
        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
