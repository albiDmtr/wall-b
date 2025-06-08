from dotenv import load_dotenv
import websockets
import os
import asyncio
import json

load_dotenv()

api_url = os.getenv('WS_API_URL', 'wss://firm-chimp-eagerly.ngrok-free.app')

async def handle_messages(websocket):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received message: {data}")

                if data.type == 'ping':
                    await websocket.send(json.dumps({'type': 'pong', 'name': 'wall-b-hardware'}))

            except json.JSONDecodeError as e:
                print(f"Failed to parse message as JSON: {e}")
                continue

    except websockets.ConnectionClosed:
        print("Connection closed")
        return

async def connect():
    while True:
        try:
            async with websockets.connect(api_url) as websocket:
                print(f"Connected to {api_url}")
                await handle_messages(websocket)
        except (websockets.ConnectionClosed, ConnectionRefusedError, OSError) as e:
            print(f"Connection failed: {str(e)}")
            await asyncio.sleep(5)
            print("Attempting to reconnect...")

def run_client():
    asyncio.run(connect())

if __name__ == "__main__":
    run_client()