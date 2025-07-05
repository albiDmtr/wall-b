import asyncio
from pyngrok import ngrok
import websockets
import json

connected_clients = set()
MCP_call_queue = None

# handle incoming websocket messages
async def message_handler(websocket):
    global connected_clients, MCP_call_queue

    connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received message: {data}")

                if data.get('type') == 'pong' or data.get('type') == 'plan-result':
                    if MCP_call_queue is not None:
                        MCP_call_queue.put(data)

            except json.JSONDecodeError:
                print(f"Received non-JSON message: {message}")
                
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def ws_queue_monitor():
    while True:
        try:
            if not MCP_call_queue.empty():
                message = MCP_call_queue.get()

                if message.get('type') == 'pong' or message.get('type') == 'plan-result':
                    # put client message back to MCP call queue
                    MCP_call_queue.put(message)
                else:
                    json_message = json.dumps(message)
                    await broadcast_message(json_message)
        except Exception as e:
            print(f"Error in queue monitor: {e}")

        await asyncio.sleep(0.1)

# broadcast message to all connected clients
async def broadcast_message(message, exclude=None):
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients]
        )

# start ws server
async def start_server():
    server = await websockets.serve(message_handler, "localhost", 8765)
    http_tunnel = ngrok.connect(addr=8765, proto="http", domain="firm-chimp-eagerly.ngrok-free.app")
    public_url = http_tunnel.public_url.replace("https://", "wss://")

    # testing
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