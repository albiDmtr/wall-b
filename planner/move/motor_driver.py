import os
os.chdir('/tmp')
os.environ['GPIOZERO_PIN_FACTORY'] = 'lgpio'

from gpiozero import Motor
import time
import atexit

# Initialize motors with their respective pins
right_motor = Motor(forward=21, backward=20)
left_motor = Motor(forward=26, backward=16)

# Ensure motors are stopped when the program exits
def cleanup():
    stop()

atexit.register(cleanup)

def left_forward():
    left_motor.forward()

def left_backward():
    left_motor.backward()

def right_forward():
    right_motor.forward()

def right_backward():
    right_motor.backward()

def stop():
    left_motor.stop()
    right_motor.stop()

def move(direction="forward"):
    if direction == "forward":
        left_forward()
        right_forward()
    elif direction == "backward":
        left_backward()
        right_backward()

def turn(direction="right"):
    if direction == "right":
        left_forward()
        right_backward()
    elif direction == "left":
        left_backward()
        right_forward()

def move_s(duration=1, direction="forward"):
    move(direction)
    time.sleep(duration)
    
    time.sleep(0.1)
    stop()

def turn_s(duration=1, side="right"):
    turn(side)
    time.sleep(duration)
    
    time.sleep(0.1)
    stop()