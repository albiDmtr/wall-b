import lgpio as GPIO
import time

TRIG = 31
ECHO = 29

h = GPIO.gpiochip_open(0)
GPIO.gpio_claim_output(h, TRIG)
GPIO.gpio_claim_input(h, ECHO)

def get_distance():
    GPIO.gpio_write(h, TRIG, 0)
    time.sleep(2)

    GPIO.gpio_write(h, TRIG, 1)
    time.sleep(0.00001)
    GPIO.gpio_write(h, TRIG, 0)

    while GPIO.gpio_read(h, ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.gpio_read(h, ECHO) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = get_distance()
            print(f"Distance: {dist} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.gpiochip_close(h)
        print("Exiting...")