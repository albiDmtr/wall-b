import evdev
from evdev import InputDevice, categorize, ecodes

def list():
	devices = [evdev.InputDevice(path) for path in evdev.list_devices()] 
	for device in devices:
		print(f"Device: {device.path}, Name: {device.name}, Phys: {device.phys}")

list()