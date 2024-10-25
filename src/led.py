import RPi.GPIO as GPIO
import time

# Set the pin number to use (for example, GPIO 18)
PIN = 26

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(PIN, GPIO.OUT)  # Set the pin as an output

try:
    while True:
        # Turn the pin ON
        GPIO.output(PIN, GPIO.HIGH)
        print("LED ON")
        time.sleep(1)  # Wait for 1 second
        
        # Turn the pin OFF
        GPIO.output(PIN, GPIO.LOW)
        print("LED OFF")
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    print("Exiting program")

finally:
    GPIO.cleanup()  # Reset GPIO settings when done