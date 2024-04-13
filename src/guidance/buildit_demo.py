import RPi.GPIO as GPIO
import time

# Pin Definitions
pin_stay_on = 17  # GPIO pin to stay on constantly
pin_blink = 22   # GPIO pin to blink

# Setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setwarnings(False)  # Disable warnings to avoid clutter

# Setup Pins
GPIO.setup(pin_stay_on, GPIO.OUT)
GPIO.setup(pin_blink, GPIO.OUT)

# Turn on the pin_stay_on continuously
GPIO.output(pin_stay_on, True)
print(f"GPIO pin {pin_stay_on} is on continuously.")

# Blinking Loop for pin_blink
try:
    while True:
        # Turn on pin_blink
        GPIO.output(pin_blink, True)
        print(f"GPIO pin {pin_blink} is on.")
        time.sleep(0.5)  # On for 0.5 seconds

        # Turn off pin_blink
        GPIO.output(pin_blink, False)
        print(f"GPIO pin {pin_blink} is off.")
        time.sleep(0.5)  # Off for 0.5 seconds

except KeyboardInterrupt:
    # Clean up GPIO settings when the user hits Ctrl+C
    print("Exiting program.")
    GPIO.cleanup()

except:
    # Clean up GPIO settings on any other error.
    print("An error occurred. Cleaning up...")
    GPIO.cleanup()