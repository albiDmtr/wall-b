import RPi.GPIO as GPIO
import pygame

# Pin setup
left_wheel_pin = 17
right_wheel_pin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(right_wheel_pin, GPIO.OUT, initial=GPIO.HIGH)

# Pygame setup
pygame.init()
size = (10, 10)  # Small window
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.display.set_caption("Wheel Control Test")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                GPIO.output(left_wheel_pin, GPIO.LOW)
                print("Left wheel is ON")
            elif event.key == pygame.K_LEFT:
                GPIO.output(right_wheel_pin, GPIO.LOW)
                print("Right wheel is ON")
            elif event.key == pygame.K_UP:
                GPIO.output(left_wheel_pin, GPIO.LOW)
                GPIO.output(right_wheel_pin, GPIO.LOW)
                print("Both wheels are ON")
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP]:
                GPIO.output(left_wheel_pin, GPIO.HIGH)
                GPIO.output(right_wheel_pin, GPIO.HIGH)
                print("Wheels are OFF")

pygame.quit()
GPIO.cleanup()  # Clean up GPIO on closing
