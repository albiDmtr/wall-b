import os
import signal
import sys
import atexit
os.chdir('/tmp')
os.environ['GPIOZERO_PIN_FACTORY'] = 'lgpio'

from gpiozero import Motor
import time

# Initialize motors with their respective pins
right_motor = Motor(forward=21, backward=20)
left_motor = Motor(forward=26, backward=16)

# Flag to track if cleanup has been performed
_cleanup_done = False

def cleanup():
    global _cleanup_done
    if not _cleanup_done:
        try:
            # Stop all motors
            left_motor.stop()
            right_motor.stop()
            
            # Close motor connections
            left_motor.close()
            right_motor.close()
            
            _cleanup_done = True
            print("Motor cleanup completed")
        except Exception as e:
            print(f"Error during cleanup: {e}")

def signal_handler(signum, frame):
    print(f"\nReceived signal {signum}, cleaning up...")
    cleanup()
    sys.exit(0)

# Register cleanup functions
atexit.register(cleanup)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

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
    time.sleep(0.1)

def move(direction="forward"):
    if direction == "forward":
        left_forward()
        right_forward()
    elif direction == "backward":
        left_backward()
        right_backward()
    else:
        print(f"Invalid direction: {direction}")


def turn(direction="right"):
    if direction == "right":
        left_forward()
        right_backward()
    elif direction == "left":
        left_backward()
        right_forward()
    else:
        print(f"Invalid turn direction: {direction}")

def move_s(duration=1, direction="forward"):
    move(direction)
    time.sleep(duration)
    stop()

def turn_s(duration=1, side="right"):
    turn(side)
    time.sleep(duration)
    stop()