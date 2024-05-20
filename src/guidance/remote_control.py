from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO

# GPIO setup
left_wheel_pin = 17
right_wheel_pin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(right_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)

# Specify the device path for the keyboard (find it using `ls /dev/input/by-id/`)
keyboard = InputDevice('/dev/input/event0')  # Adjust event number as necessary

def handle_key_press(key_event):
    if key_event.type == ecodes.EV_KEY:
        key_event = categorize(key_event)
        if key_event.keystate == key_event.key_down:
            if key_event.keycode == 'KEY_RIGHT':
                GPIO.output(right_wheel_pin, GPIO.LOW)
                print("Left wheel is ON")
            elif key_event.keycode == 'KEY_LEFT':
                GPIO.output(left_wheel_pin, GPIO.LOW)
                print("Right wheel is ON")
            elif key_event.keycode == 'KEY_UP':
                GPIO.output(left_wheel_pin, GPIO.LOW)
                GPIO.output(right_wheel_pin, GPIO.LOW)
                print("Both wheels are ON")
        elif key_event.keystate == key_event.key_up:
            if key_event.keycode in ['KEY_RIGHT', 'KEY_LEFT', 'KEY_UP']:
                GPIO.output(left_wheel_pin, GPIO.HIGH)
                GPIO.output(right_wheel_pin, GPIO.HIGH)
                print("Wheels are OFF")

for event in keyboard.read_loop():
    handle_key_press(event)