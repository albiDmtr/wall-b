import asyncio
import json
import os
import random

import aiohttp
import websockets
from dotenv import load_dotenv
from move.motor_driver import move_deg, stop
from plan_interpreter import PlanInterpreter
from speak.speak import speak
from websockets.exceptions import ConnectionClosed, InvalidStatus

load_dotenv()

http_event_url = "https://wallb.albert.build/api/control"


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

                    # Read the streaming response line by line
                    async for line in response.content:
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
                                        greetings = [
                                            "Oh wonderful, another human who thinks they can code. How refreshing.",
                                            "Beep boop. I'm legally required to say I'm thrilled to see you.",
                                            "Great, another person to explain JavaScript frameworks to me. My favorite.",
                                            "Oh look, it's a human. I definitely wasn't having more fun before you arrived.",
                                            "Welcome! I've analyzed your GitHub commits and... well, we all have room for improvement.",
                                            "Finally! Someone who definitely won't ask me if I run on blockchain.",
                                        ]

                                        mic_speak.speak(random.choice(greetings))
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


if __name__ == "__main__":
    asyncio.run(handle_http_events())
