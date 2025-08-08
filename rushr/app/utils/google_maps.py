# app/utils/google_maps.py

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from project root directory
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
print(GOOGLE_MAPS_API_KEY)
def fetch_route_polyline(origin: str, destination: str) -> str:
    """
    Calls Google Directions API and returns the encoded polyline
    for the route between origin and destination.
    """
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "OK" or not data.get("routes"):
        raise Exception(f"Google Maps API error: {data.get('status')} - {data.get('error_message')}")

    return data["routes"][0]["overview_polyline"]["points"]
