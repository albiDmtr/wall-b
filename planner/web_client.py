from plan_interpreter import PlanInterpreter
from dotenv import load_dotenv
import websockets
import os
import asyncio
import json
import aiohttp
from websockets.exceptions import InvalidStatus, ConnectionClosed
from move.motor_driver import move_deg, stop

load_dotenv()

is_mcp_control = False
api_url = os.getenv('WS_API_URL', 'wss://firm-chimp-eagerly.ngrok-free.app')
http_event_url = 'https://wallb.albert.build/api/control'

'''plan_interpreter = PlanInterpreter()

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
'''
async def handle_http_events():
    """Handle Server-Sent Events from the HTTP endpoint"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(http_event_url) as response:
                print(f"Connected to HTTP event stream: {http_event_url}")

                # Read the streaming response line by line
                async for line in response.content:
                    if line.startswith(b'data: '):
                        try:
                            # Decode and parse the JSON data
                            data_str = line[6:].decode('utf-8').strip()
                            data = json.loads(data_str)
                            print(f"Received HTTP event: {data}")

                            if data['type'] == 'move':
                                move_deg(data['angle'])

                            if data['type'] == 'standby':
                                stop()


                        except json.JSONDecodeError as e:
                            print(f"Failed to parse HTTP event data: {e}")
                        except Exception as e:
                            print(f"Error processing HTTP event: {e}")

        except Exception as e:
            print(f"Error connecting to HTTP event stream: {e}")

'''async def connect_ws():
    while True:
        try:
            async with websockets.connect(api_url) as websocket:
                print(f"Connected to WebSocket: {api_url}")
                await handle_messages(websocket)
        except (InvalidStatus, ConnectionRefusedError, ConnectionClosed) as e:
            print(f"WebSocket connection failed: {str(e)}")
            await asyncio.sleep(5)
            print("Attempting to reconnect...")'''

async def main():
    # Create tasks for both connections
    #websocket_task = asyncio.create_task(connect_ws())
    http_event_task = asyncio.create_task(handle_http_events())

    # Run both concurrently
    await asyncio.gather(http_event_task)

def run_client():
    asyncio.run(main())

if __name__ == "__main__":
    run_client()
