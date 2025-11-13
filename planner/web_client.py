import asyncio
import json
import os

import aiohttp
import websockets
from dotenv import load_dotenv
from move.motor_driver import move_deg, stop
from plan_interpreter import PlanInterpreter
from speak.speak import speak
from websockets.exceptions import ConnectionClosed, InvalidStatus

load_dotenv()

is_mcp_control = False
api_url = os.getenv("WS_API_URL", "wss://firm-chimp-eagerly.ngrok-free.app")
http_event_url = "https://wallb.albert.build/api/control"

"""plan_interpreter = PlanInterpreter()

async def handle_messages(websocket):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received WebSocket message: {data}")

                if 'type' not in data:
                    print("Message does not have a 'type' attribute")
                    print(f"Message content: {data}")
                    continue
                elif data['type'] == 'ping':
                    await websocket.send(json.dumps({'type': 'pong', 'name': 'wall-b-hardware'}))
                    print("Sent pong response")
                elif data['type'] == 'plan':
                    logs = plan_interpreter.execute(data['plan'])
                    await websocket.send(json.dumps({'type': 'plan-result', 'log': logs}))

            except json.JSONDecodeError as e:
                print(f"Failed to parse WebSocket message as JSON: {e}")
                continue

    except websockets.ConnectionClosed:
        print("WebSocket connection closed")
        return
"""


async def handle_http_events():
    print("Loading speech model...")
    mic_speak = speak()
    print("Speech model loaded. Connecting to HTTP event stream...")
    """Handle Server-Sent Events from the HTTP endpoint"""

    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(http_event_url) as response:
                    print(f"Connected to HTTP event stream: {http_event_url}")

                    # Set a random reconnect time between 20-30 seconds
                    import random

                    reconnect_time = random.randint(20, 30)
                    start_time = asyncio.get_event_loop().time()

                    # Read the streaming response line by line
                    async for line in response.content:
                        # Check if it's time to reconnect
                        if (
                            asyncio.get_event_loop().time() - start_time
                            > reconnect_time
                        ):
                            print(f"Reconnecting after {reconnect_time} seconds")
                            stop()
                            break

                        if line.startswith(b"data: "):
                            try:
                                # Decode and parse the JSON data
                                data_str = line[6:].decode("utf-8").strip()
                                data = json.loads(data_str)
                                print(f"Received HTTP event: {data}")

                                if data["type"] == "move":
                                    move_deg(data["angle"])

                                if data["type"] == "speak":
                                    mic_speak.speak(data["text"])

                                if data["type"] == "action":
                                    if data["action"] == "stuck":
                                        mic_speak.speak("Help stepbro, I'm stuck!")

                                if data["type"] == "standby":
                                    stop()

                            except json.JSONDecodeError as e:
                                print(f"Failed to parse HTTP event data: {e}")
                                stop()
                                break
                            except Exception as e:
                                print(f"Error processing HTTP event: {e}")
                                stop()
                                break

        except Exception as e:
            print(f"Error connecting to HTTP event stream: {e}")
        # Wait 5 seconds before reconnecting
        await asyncio.sleep(5)


"""async def connect_ws():
    while True:
        try:
            async with websockets.connect(api_url) as websocket:
                print(f"Connected to WebSocket: {api_url}")
                await handle_messages(websocket)
        except (InvalidStatus, ConnectionRefusedError, ConnectionClosed) as e:
            print(f"WebSocket connection failed: {str(e)}")
            await asyncio.sleep(5)
            print("Attempting to reconnect...")"""


async def main():
    # Create tasks for both connections
    # websocket_task = asyncio.create_task(connect_ws())
    http_event_task = asyncio.create_task(handle_http_events())

    # Run both concurrently
    await asyncio.gather(http_event_task)


def run_client():
    asyncio.run(main())


if __name__ == "__main__":
    run_client()
