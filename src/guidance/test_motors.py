import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setwarnings(False)

# Define GPIO pins for Motor 1
Motor1A = 17  # Input A
Motor1B = 18  # Input B
Motor1E = 27  # Enable A

# Define GPIO pins for Motor 2
Motor2A = 22  # Input A
Motor2B = 23  # Input B
Motor2E = 24  # Enable B

# Set up the motor pins:
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

# Function to run a motor
def motor_forward(motor, enable):
    GPIO.output(motor[0], True)
    GPIO.output(motor[1], False)
    GPIO.output(enable, True)

def motor_reverse(motor, enable):
    GPIO.output(motor[0], False)
    GPIO.output(motor[1], True)
    GPIO.output(enable, True)

def motor_stop(motor, enable):
    GPIO.output(motor[0], False)
    GPIO.output(motor[1], False)
    GPIO.output(enable, False)

try:
    while True:
        # Motor 1 forward
        motor_forward((Motor1A, Motor1B), Motor1E)
        time.sleep(2)

        # Motor 1 reverse
        motor_reverse((Motor1A, Motor1B), Motor1E)
        time.sleep(2)

        # Motor 2 forward
        motor_forward((Motor2A, Motor2B), Motor2E)
        time.sleep(2)

        # Motor 2 reverse
        motor_reverse((Motor2A, Motor2B), Motor2E)
        time.sleep(2)

        # Stop Motors
        motor_stop((Motor1A, Motor1B), Motor1E)
        motor_stop((Motor2A, Motor2B), Motor2E)
        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit

