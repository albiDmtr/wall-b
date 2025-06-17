import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import move.motor_driver

def back_and_forth():
    move.motor_driver.move_s(4, "forward")
    move.motor_driver.move_s(4, "backward")

def turn_left_and_right():
    move.motor_driver.turn("right")
    time.sleep(4)
    move.motor_driver.stop()
    time.sleep(0.4)
    move.motor_driver.turn("left")
    time.sleep(4)
    move.motor_driver.stop()
    time.sleep(0.4)

try:
    move.motor_driver.turn_s(4, "left")
except KeyboardInterrupt:
    print("Exiting program")