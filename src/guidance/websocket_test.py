import RPi.GPIO as GPIO
import pygame

left_wheel_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_wheel_pin, GPIO.OUT)

pygame.init()
size = (200, 100)  # Small window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Wheel Control Test")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  # Right arrow key
                GPIO.output(left_wheel_pin, False)  # Turn on the left wheel
                print("Left wheel is ON")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:  # Right arrow key released
                GPIO.output(left_wheel_pin, True)  # Turn off the left wheel
                print("Left wheel is OFF")

pygame.quit()
GPIO.cleanup()  # Clean up GPIO on closing