import RPi.GPIO as GPIO
import time

right_IN1 = 21
right_IN2 = 20
left_IN1 = 16
left_IN2 = 26

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(right_IN1, GPIO.OUT)
GPIO.setup(right_IN2, GPIO.OUT)
GPIO.setup(left_IN1, GPIO.OUT)
GPIO.setup(left_IN2, GPIO.OUT)

def left_forward():
    GPIO.output(left_IN1, GPIO.HIGH)
    GPIO.output(left_IN2, GPIO.LOW)

def left_backward():
    GPIO.output(left_IN1, GPIO.LOW)
    GPIO.output(left_IN2, GPIO.HIGH)

def right_forward():
    GPIO.output(right_IN1, GPIO.HIGH)
    GPIO.output(right_IN2, GPIO.LOW)

def right_backward():
    GPIO.output(right_IN1, GPIO.LOW)
    GPIO.output(right_IN2, GPIO.HIGH)

def stop():
    GPIO.output(right_IN1, GPIO.LOW)
    GPIO.output(right_IN2, GPIO.LOW)
    GPIO.output(left_IN1, GPIO.LOW)
    GPIO.output(left_IN2, GPIO.LOW)

def move(direction = "forward"):
    if direction == "forward":
        left_forward()
        right_forward()
    elif direction == "backward":
        left_backward()
        right_backward()

def turn(direction = "right"):
    if direction == "right":
        left_forward()
        right_backward()
    elif direction == "left":
        left_backward()
        right_forward()