from pynput.keyboard import Key, Listener
import RPi.GPIO as GPIO

# GPIO setup
left_wheel_pin = 17
right_wheel_pin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(right_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)

def on_press(key):
    try:
        if key == Key.right:
            GPIO.output(left_wheel_pin, GPIO.LOW)
            print("Left wheel is ON")
        elif key == Key.left:
            GPIO.output(right_wheel_pin, GPIO.LOW)
            print("Right wheel is ON")
        elif key == Key.up:
            GPIO.output(left_wheel_pin, GPIO.LOW)
            GPIO.output(right_wheel_pin, GPIO.LOW)
            print("Both wheels are ON")
    except AttributeError:
        pass

def on_release(key):
    if key in [Key.right, Key.left, Key.up]:
        GPIO.output(left_wheel_pin, GPIO.HIGH)
        GPIO.output(right_wheel_pin, GPIO.HIGH)
        print("Wheels are OFF")
    if key == Key.esc:  # Press escape to stop the listener
        return False

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

GPIO.cleanup()  # Clean up GPIO on closing

