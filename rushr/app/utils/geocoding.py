import os
import requests
from typing import Dict

# This function can be in a file like app/utils/geocoding.py

def get_search_params(origin: str, destination: str) -> Dict[str, float]:
    """
    Takes text-based start and end locations, geocodes them,
    and returns a dictionary of lat/lon parameters for the search API.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("Google Maps API key is not set in environment variables.")

    def _geocode(address: str) -> Dict[str, float]:
        """Helper function to geocode a single address."""
        print(f"Geocoding address: '{address}'...")
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for bad status codes
        
        data = response.json()
        if data['status'] != 'OK' or not data.get('results'):
            raise ConnectionError(f"Could not find coordinates for '{address}'. Status: {data['status']}")
            
        location = data['results'][0]['geometry']['location']
        print(f"Found coordinates: {location}")
        return {"lat": location['lat'], "lon": location['lng']}

    try:
        start_coords = _geocode(origin)
        end_coords = _geocode(destination)

        return {
            "start_lat": start_coords["lat"],
            "start_lon": start_coords["lon"],
            "end_lat": end_coords["lat"],
            "end_lon": end_coords["lon"],
        }
    except (requests.exceptions.RequestException, ConnectionError) as e:
        print(f"Error during geocoding: {e}")
        # Depending on your needs, you might return None or re-raise the exception
        return None