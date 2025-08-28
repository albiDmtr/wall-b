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

def move_deg(angle, speed=1.0):
    """
    Move the robot in a specific direction based on angle.

    Args:
        angle (float): Direction in degrees (-180 to 180)
                      0 = forward, 90 = right, -90 = left, ±180 = backward
        speed (float): Overall speed factor (0.0 to 1.0)
    """
    import math

    # Normalize angle to -180 to 180 range
    angle = ((angle + 180) % 360) - 180

    # Convert to radians
    angle_rad = math.radians(angle)

    # Calculate left and right motor speeds using trigonometry
    # We use sin and cos to get the contribution of forward/backward movement
    # Left motor: forward speed increases with cos(angle) + sin(angle)
    # Right motor: forward speed increases with cos(angle) - sin(angle)
    left_speed = speed * (math.cos(angle_rad) + math.sin(angle_rad))
    right_speed = speed * (math.cos(angle_rad) - math.sin(angle_rad))

    # Clamp speeds to [-1, 1] range
    left_speed = max(-1.0, min(1.0, left_speed))
    right_speed = max(-1.0, min(1.0, right_speed))

    # Apply speeds to motors
    if left_speed >= 0:
        left_motor.forward(left_speed)
    else:
        left_motor.backward(abs(left_speed))

    if right_speed >= 0:
        right_motor.forward(right_speed)
    else:
        right_motor.backward(abs(right_speed))
