# Weather Travel Agent – Groq + FastMCP + Open-Meteo

A minimal but clean **travel/weather conversational agent** that:

- Takes natural language input ("What's the weather like in Kochi tomorrow?", "Is it raining in Delhi?")
- Uses **Groq + Llama 3.1 8B** to understand intent and decide whether to call a tool
- Calls a **local FastMCP microservice** to get real current weather
- Returns a natural language answer

Built as a demonstration of **tool-calling** + **local tool server** pattern.

## Project Goals

- Show clean separation between LLM logic and tool implementation
- Use **FastMCP** for simple, typed, local tool serving (STDIO + HTTP modes)
- Demonstrate **function calling / tool use** with Groq API
- Keep everything lightweight and runnable on a laptop

## Server set-up

| Command             | What it does                                                   |
| ------------------- | -------------------------------------------------------------- |
| uv init .           | Creates a Python project in the current folder                 |
| uv add "mcp[cli]"   | Installs MCP with command-line tools                           |
| uv add "geopy"      | Installs geolocation library for converting city → coordinates |


## Folder Structure

travel-agent/
├── src/
│   ├── tools/
│   │   └── pycache/
│   │
│   ├── weather_client.py     ← Client that talks to FastMCP weather service
│   └── agent.py              ← Main agent logic (Groq + tool calling loop)
│
├── weather-mcp/              ← The weather tool microservice (FastMCP server)
│   ├── .venv/
│   ├── .gitignore
│   ├── main.py               ← FastMCP server + Open-Meteo logic
│   ├── pyproject.toml
│   ├── README.md             (this file – you can keep a copy here too)
│   ├── uv.lock
│   └── requirements.txt
│
└── README.md                 ← Main documentation (recommended root location)

### Quick File Role Summary

| File                  | Role                                                                   | Runs as          | Talks to                   |
|-----------------------|------------------------------------------------------------------------|------------------|----------------------------|
| agent.py              | LLM conversation loop + tool decision + final natural answer           | Client script    | Groq API + weather-mcp     |
| weather_client.py     |  Async/sync wrapper to call the FastMCP weather tool                   | Library          | http://127.0.0.1:8001      |
| weather-mcp/main.py   | FastMCP server exposing open_weather_app tool + Open-Meteo client      | HTTP server      | open-meteo.com + Nominatim |

## How It Works – Step-by-step Flow

mermaid
flowchart TD

A[You type: "Weather in Paris?"] --> B[agent.py]

B --> C[Send prompt + tool schema to Groq<br>model = llama-3.1-8b-instant]

C --> D{Model decides}

D -->|No tool needed| E[Return direct answer]
D -->|Call tool| F[Tool call: get_current_weather<br>→ query = "weather in Paris"]

F --> G[agent.py calls get_weather_sync(...)]

G --> H[weather_client.py → HTTP POST to<br>http://127.0.0.1:8001/mcp]

H --> I[FastMCP server weather-mcp/main.py]

I --> J[Extract location from query<br>e.g. "Paris"]

J --> K[Geocode → Nominatim<br>→ lat,lon]

K --> L[Call Open-Meteo API<br>current_weather=true]

L --> M[Map weathercode → description<br>Format nice dict]

M --> N[Return JSON-like dict to client]

N --> O[agent.py appends tool result to messages]

O --> P[Second Groq call<br>with tool result included]

P --> Q[Model generates natural final answer]

Q --> R[You see: "In Paris right now it's 14°C, partly cloudy..."]


LLM           : Groq API (Llama 3.1 8B Instruct)

Tool protocol : FastMCP (lightweight local tool server)

Weather       : Open-Meteo (free, excellent, no API key)

Geocoding     : Nominatim (OpenStreetMap)

HTTP client   : requests (in main.py) + fastmcp Client (in weather_client.py)

Environment   : python-dotenv + GROQ_API_KEY







hey hello!,