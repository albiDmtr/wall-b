from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time
import subprocess

# GPIO setup
left_wheel_pin = 17
#left_wheel_pin_back = 27
right_wheel_pin = 22
button_pin = 16
#right_wheel_pin_back = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(right_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(left_wheel_pin_back, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.setup(right_wheel_pin_back, GPIO.OUT, initial=GPIO.HIGH)

# Specify the device path for the keyboard (find it using `ls /dev/input/by-id/`)
keyboard = InputDevice('/dev/input/event0')  # Adjust event number as necessary

def handle_key_press(key_event):
    if key_event.type == ecodes.EV_KEY:
        key_event = categorize(key_event)
        if key_event.keystate == key_event.key_down:
            if key_event.keycode == 'KEY_LEFT':
                GPIO.output(right_wheel_pin, GPIO.LOW)
                print("Left wheel is ON")
            elif key_event.keycode == 'KEY_RIGHT':
                GPIO.output(left_wheel_pin, GPIO.LOW)
                print("Right wheel is ON")
            elif key_event.keycode == 'KEY_UP':
                GPIO.output(left_wheel_pin, GPIO.LOW)
                GPIO.output(right_wheel_pin, GPIO.LOW)
                print("Both wheels are ON")
            #elif key_event.keycode == 'KEY_DOWN':
            #    GPIO.output(left_wheel_pin_back, GPIO.LOW)
            #    GPIO.output(right_wheel_pin_back, GPIO.LOW)
        elif key_event.keystate == key_event.key_up:
            if key_event.keycode in ['KEY_RIGHT', 'KEY_LEFT', 'KEY_UP', 'KEY_DOWN']:
                GPIO.output(left_wheel_pin, GPIO.HIGH)
                GPIO.output(right_wheel_pin, GPIO.HIGH)
                print("Wheels are OFF")

try:
    while True:
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.LOW:
            subprocess.run(["mpg321", "public\stop.mp3"])
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()        

for event in keyboard.read_loop():
    handle_key_press(event)