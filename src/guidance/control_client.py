import asyncio
import websockets
import pygame

# Set up the WebSocket connection to the Raspberry Pi server
async def control_robot():
    uri = "ws://10.100.22.126:8765"  # Updated with your Raspberry Pi's IP address
    async with websockets.connect(uri) as websocket:
        # Initialize pygame
        pygame.init()
        size = (300, 100)  # Window size
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Robot Control Interface")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # Send command to turn right motor on (robot turns left)
                        await websocket.send("right")
                        print("Sending command: right")
                    elif event.key == pygame.K_RIGHT:
                        # Send command to turn left motor on (robot turns right)
                        await websocket.send("left")
                        print("Sending command: left")
                    elif event.key == pygame.K_UP:
                        # Send command to turn both motors on
                        await websocket.send("both")
                        print("Sending command: both")
                    elif event.key == pygame.K_DOWN:
                        # Send command to stop both motors
                        await websocket.send("stop")
                        print("Sending command: stop")

        pygame.quit()

if __name__ == "__main__":
    asyncio.run(control_robot())
