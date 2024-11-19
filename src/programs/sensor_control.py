from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time

trig_pin = 10
front_sensor_pin = 9


GPIO.setmode(GPIO.BCM)
GPIO.setup(trig_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(front_sensor_pin, GPIO.IN)

def distance(sensor_pin):
	startTime = time.time()
	stopTime = time.time()	
	
	GPIO.output(trig_pin, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(trig_pin, GPIO.LOW)
	
	while GPIO.input(sensor_pin) == GPIO.LOW:
		startTime = time.time()
	
	while GPIO.input(sensor_pin) == GPIO.HIGH:
		stopTime = time.time()
	
		
	elapsedTime = stopTime - startTime
	distance = elapsedTime * 17150
	
	
	
	print(distance)
	
while True:	
	distance(front_sensor_pin)  
	time.sleep(1/4)
