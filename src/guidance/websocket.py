import asyncio
import websockets
import RPi.GPIO as GPIO

# Define GPIO pins for the motors
left_wheel_pin = 17
right_wheel_pin = 22

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_wheel_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(right_wheel_pin, GPIO.OUT, initial=GPIO.LOW)

async def control_robot(websocket, path):
    async for message in websocket:
        print(f"Received command: {message}")
        if message == "left":
            GPIO.output(left_wheel_pin, GPIO.HIGH)  # Turn on left motor
            GPIO.output(right_wheel_pin, GPIO.LOW)  # Ensure right motor is off
            print("Left motor on")
        elif message == "right":
            GPIO.output(right_wheel_pin, GPIO.HIGH)  # Turn on right motor
            GPIO.output(left_wheel_pin, GPIO.LOW)    # Ensure left motor is off
            print("Right motor on")
        elif message == "both":
            GPIO.output(left_wheel_pin, GPIO.HIGH)   # Turn on both motors
            GPIO.output(right_wheel_pin, GPIO.HIGH)
            print("Both motors on")
        else:
            # Turn off both motors
            GPIO.output(left_wheel_pin, GPIO.LOW)
            GPIO.output(right_wheel_pin, GPIO.LOW)
            print("Motors off")
            response = "Motors off or unknown command"
            await websocket.send(response)

async def main():
    try:
        server = await websockets.serve(control_robot, '0.0.0.0', 8765)
        print("WebSocket server started on ws://0.0.0.0:8765")
        await server.wait_closed()
    finally:
        # Clean up GPIO settings before closing
        GPIO.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    asyncio.run(main())
