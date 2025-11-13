import asyncio
import json
import os

import aiohttp
import websockets
from dotenv import load_dotenv
from plan_interpreter import PlanInterpreter
from websockets.exceptions import ConnectionClosed, InvalidStatus

load_dotenv()

api_url = os.getenv("WS_API_URL", "wss://firm-chimp-eagerly.ngrok-free.app")

plan_interpreter = PlanInterpreter()


async def handle_messages(websocket):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received WebSocket message: {data}")

                if "type" not in data:
                    print("Message does not have a 'type' attribute")
                    print(f"Message content: {data}")
                    continue
                elif data["type"] == "ping":
                    await websocket.send(
                        json.dumps({"type": "pong", "name": "wall-b-hardware"})
                    )
                    print("Sent pong response")
                elif data["type"] == "plan":
                    logs = plan_interpreter.execute(data["plan"])
                    await websocket.send(
                        json.dumps({"type": "plan-result", "log": logs})
                    )

            except json.JSONDecodeError as e:
                print(f"Failed to parse WebSocket message as JSON: {e}")
                continue

    except websockets.ConnectionClosed:
        print("WebSocket connection closed")
        return


async def connect_ws():
    while True:
        try:
            async with websockets.connect(api_url) as websocket:
                print(f"Connected to WebSocket: {api_url}")
                await handle_messages(websocket)
        except (InvalidStatus, ConnectionRefusedError, ConnectionClosed) as e:
            print(f"WebSocket connection failed: {str(e)}")
            await asyncio.sleep(5)
            print("Attempting to reconnect...")


if __name__ == "__main__":
    asyncio.run(connect_ws())
