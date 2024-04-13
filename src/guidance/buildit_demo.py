from gpiozero import LED
from time import sleep

left_wheel = LED(17)
right_wheel = LED(22)

right_wheel.on()
while True:
    left_wheel.on()
    sleep(0.5)
    left_wheel.off()
    sleep(0.5)