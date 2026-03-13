# import asyncio
# from fastmcp import Client
# from pathlib import Path


# # Absolute path to your weather MCP server
# WEATHER_SERVER_PATH = Path(__file__).resolve().parents[3] / "weather-mcp" / "main.py"


# async def get_weather(query: str):
#     """
#     Connects to Weather MCP server and calls open_weather_app tool.
#     """

#     async with Client(f"python {WEATHER_SERVER_PATH}") as client:

#         # Optional: see available tools
#         # tools = await client.list_tools()
#         # print(tools)

#         result = await client.call_tool(
#             "open_weather_app",
#             {"query": query}
#         )

#         return result


# # Helper for synchronous usage
# def get_weather_sync(query: str):
#     return asyncio.run(get_weather(query))



import asyncio
from fastmcp import Client


async def get_weather(query: str):

    async with Client("http://127.0.0.1:8001/mcp") as client:
        result = await client.call_tool(
            "open_weather_app",
            {"query": query}
        )

        return result


def get_weather_sync(query: str):
    return asyncio.run(get_weather(query))