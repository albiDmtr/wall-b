# server.py
import os
import time

import requests
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Wall-B-Control")


def read_md(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    markdown_path = os.path.join(current_dir, filename)
    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


@mcp.tool()
def get_plandocs() -> str:
    """Get general information about the Wall-B robot and documentation about the planning language required by the control tool."""
    plandocs = read_md("plandocs.md")
    return plandocs


@mcp.tool()
def check_online() -> bool:
    """Check if the Wall-B robot is turned on an online"""
    response = requests.post(
        "https://wallb.albert.build/api/mcp",
        json={"type": "ping"},
        timeout=3,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("name") == "wall-b-hardware" and data.get("type") == "pong"


@mcp.tool()
def control(plan: str) -> str:
    """Submit commands to Wall-B the robot in the required format.
    Always check the documentation for the required format of the plan before using this tool.
    Returns logs ending with `[Plan executed successfully]` if plan execution was successful, an error or status message if it wasn't.
    """

    response = requests.post(
        "https://wallb.albert.build/api/mcp",
        json={"type": "plan", "text": plan},
        timeout=3,
    )

    while (not response) {
        # do stuff here
        time.sleep(1.5)
    }

    if response is None:
        return "Error: No response from Wall-B robot within the timeout period."
    else:
        return response.get("log")


if __name__ == "__main__":
    mcp.run(transport="stdio")
