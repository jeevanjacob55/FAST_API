
import os
import requests
from dotenv import load_dotenv
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
print(GOOGLE_MAPS_API_KEY)
from app.utils.google_maps import fetch_route_polyline

def test_polyline_fetch():
    origin = "Kochi, IN"
    destination = "Bangalore, IN"
    
    try:
        polyline = fetch_route_polyline(origin, destination)
        assert isinstance(polyline, str) and len(polyline) > 0
        print("✅ Test Passed: Polyline fetched successfully.")
    except Exception as e:
        print(f"❌ Test Failed: {e}")

test_polyline_fetch()
