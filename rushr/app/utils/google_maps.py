# app/utils/google_maps.py

import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict

# Load .env file from project root directory
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
print(GOOGLE_MAPS_API_KEY)

def get_coordinates_for_address(address: str) -> Dict[str, float]:
    """Helper function to geocode a single address."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("Google Maps API key is not set.")
        
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    if data['status'] != 'OK' or not data.get('results'):
        raise ConnectionError(f"Could not find coordinates for '{address}'")
        
    location = data['results'][0]['geometry']['location']
    return {"lat": location['lat'], "lon": location['lng']}

# ... your fetch_route_polyline function can also be in this file ...


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
