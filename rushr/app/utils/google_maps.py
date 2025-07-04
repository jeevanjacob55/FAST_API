# app/utils/google_maps.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


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

    if data["status"] != "OK" or not data["routes"]:
        raise Exception("Failed to fetch route from Google Maps")

    return data["routes"][0]["overview_polyline"]["points"]
