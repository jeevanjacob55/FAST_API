# app/api/rides.py

import asyncio
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import RideCreate, RideOut, RideSearch
from app.models import Ride
from app.utils.google_maps import fetch_route_polyline, get_coordinates_for_address
from app.utils.matching import route_matches

router = APIRouter()

# --- PUBLISH ENDPOINT (No changes needed, but kept for context) ---
@router.post("/publish/", response_model=RideOut)
def publish_ride(ride: RideCreate, db: Session = Depends(get_db)):
    try:
        polyline = fetch_route_polyline(ride.leaving_from, ride.going_to)
        if not polyline:
            raise HTTPException(status_code=400, detail="Could not generate route polyline.")
        
        new_ride = Ride(
            leaving_from=ride.leaving_from,
            going_to=ride.going_to,
            seats=ride.seats,
            driver_id=1,
            polyline=polyline,
        )
        db.add(new_ride)
        db.commit()
        db.refresh(new_ride)
        return new_ride
    except Exception as e:
        print(f"!!! ERROR in /publish: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred during ride publishing.")


# --- SEARCH ENDPOINT (WITH DETAILED LOGGING) ---
@router.post("/search", response_model=List[RideOut])
async def search_rides(search: RideSearch, db: Session = Depends(get_db), tolerance_km: float = 5.0):
    """
    Geocodes text locations and then searches for matching rides.
    """
    print("\n--- ENTERING /search ENDPOINT (Text Search) ---")
    print(f"DEBUG: Received search request for: {search.leaving_from} -> {search.going_to}")

    try:
        # Step 1: Geocode the start and end locations asynchronously
        # We run them concurrently for better performance
        start_task = asyncio.to_thread(get_coordinates_for_address, search.leaving_from)
        end_task = asyncio.to_thread(get_coordinates_for_address, search.going_to)
        
        start_coords, end_coords = await asyncio.gather(start_task, end_task)
        
        print(f"DEBUG: Geocoded start: {start_coords}, end: {end_coords}")

    except Exception as e:
        print(f"!!! ERROR during geocoding: {e}")
        raise HTTPException(status_code=400, detail=f"Could not find coordinates: {e}")

    # The coordinates are now ready for the existing matching logic
    passenger_start = (start_coords["lat"], start_coords["lon"])
    passenger_end = (end_coords["lat"], end_coords["lon"])

    # Step 2: The rest of the logic remains the same
    def _find_matches_in_db():
        print("DEBUG: [Thread] Querying database for active rides...")
        rides = db.query(Ride).filter(Ride.polyline.isnot(None), Ride.seats > 0).all()
        print(f"DEBUG: [Thread] Found {len(rides)} potential rides.")
        
        matching_rides = []
        for ride in rides:
            if route_matches(passenger_start, passenger_end, ride.polyline, tolerance_km=tolerance_km):
                matching_rides.append(ride)
        
        return matching_rides

    try:
        matching = await asyncio.to_thread(_find_matches_in_db)
        print(f"--- EXITING /search with {len(matching)} matches ---")
        return matching
    except Exception as e:
        print(f"!!! UNHANDLED EXCEPTION in /search endpoint: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
