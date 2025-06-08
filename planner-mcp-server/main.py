# server.py
from mcp.server.fastmcp import FastMCP
import threading
import queue
import time
import os
from ws_server import run_ws_server

# queue for communication between MCP and WebSocket server
MCP_call_queue = queue.Queue()

# Create an MCP server
mcp = FastMCP("Wall-B-Control")

def read_md(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    markdown_path = os.path.join(current_dir, filename)
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

@mcp.tool()
def get_plandocs() -> str:
    """Get general imformation about the Wall-B robot and documentation about the planning language required by the control tool."""
    plandocs = read_md('plandocs.md')
    return plandocs

@mcp.tool()
def check_online() -> bool:
    """Check if the Wall-B robot is turned on an online"""
    MCP_call_queue.put({'type': 'ping'})

    start_time = time.time()
    while time.time() - start_time < 3:
        if not MCP_call_queue.empty():
            response = MCP_call_queue.get()

            if response.get('type') == 'pong' and response.get('name') == 'wall-b-hardware':
                return True
            else:
                # put non-matching messages back in queue
                MCP_call_queue.put(response)
        time.sleep(0.1)

    return False

@mcp.tool()
def control(plan: str) -> str:
    """Submit commands to Wall-B the robot in the required format.
    Returns 'success' if plan execution was successful, an error or status message if it wasn't.
    """

    # add the plan to the queue
    MCP_call_queue.put({'plan': plan})
    time.sleep(300)  # Simulate a delay for the plan to be executed

    return 'success'


def run_mcp_server():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    ws_thread = threading.Thread(target=run_ws_server, args=(MCP_call_queue,))
    mcp_thread = threading.Thread(target=run_mcp_server)
    
    ws_thread.daemon = True
    mcp_thread.daemon = True
    ws_thread.start()
    mcp_thread.start()
    
    # keep the main thread running
    try:
        while True:
            ws_thread.join(1)
            mcp_thread.join(1)
    except KeyboardInterrupt:
        print("Shutting down...")

