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

def look_for_msg(type, field_name=None, field_value=None, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = MCP_call_queue.get_nowait()

            if response.get('type') == type:
                if field_name is None or response.get(field_name) == field_value:
                    return response
                
            # put non-matching message back
            MCP_call_queue.put(response)
            
        except queue.Empty:
            time.sleep(0.1)
            continue

def read_md(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    markdown_path = os.path.join(current_dir, filename)
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

@mcp.tool()
def get_plandocs() -> str:
    """Get general information about the Wall-B robot and documentation about the planning language required by the control tool."""
    plandocs = read_md('plandocs.md')
    return plandocs

@mcp.tool()
def check_online() -> bool:
    """Check if the Wall-B robot is turned on an online"""
    MCP_call_queue.put({'type': 'ping'})

    pong = look_for_msg('pong', 'name', 'wall-b-hardware', 3)
    return (pong is not None)

@mcp.tool()
def control(plan: str) -> str:
    """Submit commands to Wall-B the robot in the required format.
    Always check the documentation for the required format of the plan before using this tool.
    Returns logs ending with `[Plan executed successfully]` if plan execution was successful, an error or status message if it wasn't.
    """

    # add the plan to the queue
    MCP_call_queue.put({'type':'plan', 'plan': plan})

    response = look_for_msg('plan-result', None, None, 300)

    if response is None:
        return "Error: No response from Wall-B robot within the timeout period."
    else:
        return response.get('log')

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

