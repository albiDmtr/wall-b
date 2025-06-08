import asyncio
from pyngrok import ngrok
import websockets
import json

connected_clients = set()
MCP_call_queue = None

# handle incoming websocket messages
async def message_handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received message: {data}")

                if data.get('type') == 'pong':
                    if MCP_call_queue is not None:
                        MCP_call_queue.put(data)

            except json.JSONDecodeError:
                print(f"Received non-JSON message: {message}")
                # Handle non-JSON messages if needed
                
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

# broadcast message to all connected clients
async def broadcast_message(message, exclude=None):
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients]
        )

async def ws_queue_monitor():
    while True:
        try:
            if not MCP_call_queue.empty():
                message = MCP_call_queue.get()
                json_message = json.dumps(message)
                await broadcast_message(json_message)
        except Exception as e:
            print(f"Error in queue monitor: {e}")

        await asyncio.sleep(0.1)

async def broadcast_public_url():
        while True:
            await asyncio.sleep(2)
            message = json.dumps({"public_url": "public_url"})
            await broadcast_message(message)

# start ws server
async def start_server():
    server = await websockets.serve(message_handler, "localhost", 8765)
    http_tunnel = ngrok.connect(addr=8765, proto="http", domain="firm-chimp-eagerly.ngrok-free.app")
    public_url = http_tunnel.public_url.replace("https://", "wss://")

    # testing
    asyncio.create_task(broadcast_public_url())
    asyncio.create_task(ws_queue_monitor())

    print("WebSocket server started at ws://localhost:8765")
    print(f"Public WebSocket URL: {public_url}")
    await server.wait_closed()

def run_ws_server(call_queue):
    global MCP_call_queue

    MCP_call_queue = call_queue
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(start_server())
    finally:
        loop.close()