from fastmcp import FastMCP
from geopy.geocoders import Nominatim
import requests
import re

# Create MCP server
mcp = FastMCP("Weather App")

# -----------------------------
# Tool Registration
# -----------------------------
@mcp.tool()
def open_weather_app(query: str):
    """
    Get information about the current weather in a specified location.
    Example queries:
    - "weather in Kochi"
    - "what is the weather in Delhi"
    """

    location_name = extract_location(query)

    lat, lon = get_lat_lon(location_name)

    if lat is None or lon is None:
        return f"Could not find location: {location_name}"

    weather_data = get_weather(lat, lon)

    return {
        "location": location_name,
        "temperature": weather_data["temperature"],
        "windspeed": weather_data["windspeed"],
        "condition": weather_data["weathercode"]
    }


# -----------------------------
# Weather Code Mapping
# -----------------------------
weathercode_desc = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    61: "Light rain",
    71: "Light snow",
    80: "Rain showers",
    95: "Thunderstorm"
}


# -----------------------------
# Fetch Weather from Open-Meteo
# -----------------------------
def get_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()
        current = data["current_weather"]
        units = data["current_weather_units"]

        temperature = f"{current['temperature']} {units['temperature']}"
        windspeed = f"{current['windspeed']} {units['windspeed']}"
        condition = weathercode_desc.get(
            current["weathercode"],
            f"Code {current['weathercode']}"
        )

        return {
            "temperature": temperature,
            "windspeed": windspeed,
            "weathercode": condition
        }

    except Exception as e:
        print(f"Weather API error: {e}")
        return {
            "temperature": "N/A",
            "windspeed": "N/A",
            "weathercode": "Unavailable"
        }


# -----------------------------
# Convert Location Name → Lat/Lon
# -----------------------------
def get_lat_lon(location_name):
    try:
        geolocator = Nominatim(user_agent="weather-mcp-app")
        location = geolocator.geocode(location_name)

        if location:
            return location.latitude, location.longitude

        return None, None

    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None


# -----------------------------
# Extract Location from Query
# -----------------------------
def extract_location(query: str) -> str:
    query = query.lower().strip()

    patterns = [
        r"weather\s+(in|at|for|about)?\s*(.+)",
        r"what(?:'s| is)? the weather (in|at|for|about)?\s*(.+)",
        r"how is the weather (in|at|for|about)?\s*(.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            location = match.group(2)
            return location.strip(" ?.,").title()

    # fallback
    return query.title()


# -----------------------------
# Run MCP Server (STDIO mode)
# -----------------------------
if __name__ == "__main__":
    mcp.run(transport="http", port=8001)   
