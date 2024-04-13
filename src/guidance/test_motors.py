import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setwarnings(False)

# Define GPIO pins for Motor 1
Motor1A = 17  # Input A
Motor1B = 18  # Input B (Not used for direction)
Motor1E = 27  # Enable A

# Define GPIO pins for Motor 2
Motor2A = 22  # Input A
Motor2B = 23  # Input B (Not used for direction)
Motor2E = 24  # Enable B

# Set up the motor pins:
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

# Function to turn on a motor
def motor_on(motor, enable):
    GPIO.output(motor[0], True)
    GPIO.output(motor[1], False)  # Not changing the direction, just ensuring it is off
    GPIO.output(enable, True)

# Function to turn off a motor
def motor_off(motor, enable):
    GPIO.output(motor[0], False)
    GPIO.output(motor[1], False)
    GPIO.output(enable, False)

try:
    while True:
        # Turn Motor 1 on
        motor_on((Motor1A, Motor1B), Motor1E)
        time.sleep(2)

        # Turn Motor 1 off
        motor_off((Motor1A, Motor1B), Motor1E)
        time.sleep(2)

        # Turn Motor 2 on
        motor_on((Motor2A, Motor2B), Motor2E)
        time.sleep(2)

        # Turn Motor 2 off
        motor_off((Motor2A, Motor2B), Motor2E)
        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
