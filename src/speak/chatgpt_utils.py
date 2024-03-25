import os
from openai import OpenAI
import json
import os

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.json')

# Read the config.json file
with open(config_path, 'r') as f:
    config = json.load(f)

# Access the OPENAI_API_KEY
OPENAI_API_KEY = config.get('OPENAI_API_KEY')

def get_greeting():

    client = OpenAI(api_key=OPENAI_API_KEY)
   
    try:
        chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI with a sense of humor, programmed to break the ice."},
            {"role": "user", "content": "Your task is to relentlessly market a hackathon called Build It to people who are in front of you. Your comments should be 16 words max."}
        ]
    )
        # Assuming the response structure is correctly handled by the library version
        greeting = chat_completion.choices[0].message.content.strip()  # Adjusted access to attributes
        return greeting
    except Exception as e:
        print(f"Error getting greeting from ChatGPT: {e}")
        return "Wazzup my homie. Welcome to Startup Sauna"

print(get_greeting())