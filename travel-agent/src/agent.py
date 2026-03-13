import os
import json
from dotenv import load_dotenv
from groq import Groq

from tools.weather_client import get_weather_sync

# Load environment variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"   # ✅ valid working Groq model

# Tool schema definition
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather information for any city or location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Weather query like 'weather in Kochi'"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def run_agent(user_input: str):

    messages = [
        {"role": "system", "content": "You are a smart travel assistant."},
        {"role": "user", "content": user_input}
    ]

    # 🔹 First LLM call (tool detection)
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # 🔥 If model wants to call tool
    if message.tool_calls:

        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments or "{}")

        # Execute tool
        if tool_name == "get_current_weather":
            result = get_weather_sync(arguments["query"])
        else:
            result = "Unknown tool"

        # Append assistant tool call message
        messages.append(message)

        # Append tool result
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

        # 🔹 Second LLM call (final natural answer)
        final_response = client.chat.completions.create(
            model=MODEL,   # ✅ same working model
            messages=messages
        )

        return final_response.choices[0].message.content

    # 🔹 If no tool call needed
    return message.content


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        response = run_agent(user_input)
        print("Agent:", response)