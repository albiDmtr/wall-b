import RPi.GPIO as GPIO
import pygame

left_wheel_pin = 17
right_wheel_pin = 22
GPIO.setmode(GPIO.BCM)

pygame.init()
size = (10, 10)  # Small window
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.display.set_caption("Wheel Control Test")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                GPIO.setup(left_wheel_pin, GPIO.OUT)
                GPIO.output(left_wheel_pin, False)
                print("Left wheel is ON")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                GPIO.setup(left_wheel_pin, GPIO.OUT)
                GPIO.output(left_wheel_pin, True)
                print("Left wheel is OFF")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                GPIO.setup(right_wheel_pin, GPIO.OUT)
                GPIO.output(right_wheel_pin, False)
                print("Right wheel is ON")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                GPIO.setup(right_wheel_pin, GPIO.OUT)
                GPIO.output(right_wheel_pin, True)
                print("Right wheel is OFF")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                GPIO.setup(left_wheel_pin, GPIO.OUT)
                GPIO.output(left_wheel_pin, False)
                GPIO.setup(right_wheel_pin, GPIO.OUT)
                GPIO.output(right_wheel_pin, False)
                print("Both wheels are ON")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                GPIO.setup(left_wheel_pin, GPIO.OUT)
                GPIO.output(left_wheel_pin, True)
                GPIO.setup(right_wheel_pin, GPIO.OUT)
                GPIO.output(right_wheel_pin, True)
                print("Both wheels are OFF")

pygame.quit()
GPIO.cleanup()  # Clean up GPIO on closing