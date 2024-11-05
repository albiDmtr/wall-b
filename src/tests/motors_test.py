import RPi.GPIO as GPIO
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import move.motor_driver

def back_and_forth():
    move.motor_driver.move("forward")
    time.sleep(1)
    move.motor_driver.stop()
    time.sleep(0.4)
    move.motor_driver.move("backward")
    time.sleep(1)
    move.motor_driver.stop()
    time.sleep(0.4)

def turn_left_and_right():
    move.motor_driver.turn("right")
    time.sleep(1)
    move.motor_driver.stop()
    time.sleep(0.4)
    move.motor_driver.turn("left")
    time.sleep(1)
    move.motor_driver.stop()
    time.sleep(0.4)

try:
    while True:
        back_and_forth()
        turn_left_and_right()

except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup() 