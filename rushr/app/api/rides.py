import asyncio
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import RideCreate, RideOut, RideSearch
from app.models import Ride, User
from app.utils.google_maps import fetch_route_polyline, get_coordinates_for_address
from app.utils.matching import route_matches
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/publish/", response_model=RideOut)
def publish_ride(
    ride: RideCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Publishes a new ride for the currently authenticated user.
    """
    try:
        polyline = fetch_route_polyline(ride.leaving_from, ride.going_to)
        if not polyline:
            raise HTTPException(status_code=400, detail="Could not generate route polyline.")
        
        new_ride = Ride(
            leaving_from=ride.leaving_from,
            going_to=ride.going_to,
            seats=ride.seats,
            driver_id=current_user.id,  # Use the ID of the logged-in user
            polyline=polyline,
        )
        db.add(new_ride)
        db.commit()
        db.refresh(new_ride)
        return new_ride
    except Exception as e:
        print(f"!!! ERROR in /publish: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred during ride publishing.")


@router.post("/search", response_model=List[RideOut])
async def search_rides(search: RideSearch, db: Session = Depends(get_db), tolerance_km: float = 5.0):
    """
    Geocodes text locations and then searches for matching rides asynchronously.
    """
    print(f"\n--- ENTERING /search for: {search.leaving_from} -> {search.going_to} ---")
    try:
        start_task = asyncio.to_thread(get_coordinates_for_address, search.leaving_from)
        end_task = asyncio.to_thread(get_coordinates_for_address, search.going_to)
        start_coords, end_coords = await asyncio.gather(start_task, end_task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not find coordinates: {e}")

    passenger_start = (start_coords["lat"], start_coords["lon"])
    passenger_end = (end_coords["lat"], end_coords["lon"])

    def _find_matches_in_db():
        rides = db.query(Ride).filter(Ride.polyline.isnot(None), Ride.seats > 0).all()
        matching_rides = []
        for ride in rides:
            if route_matches(passenger_start, passenger_end, ride.polyline, tolerance_km=tolerance_km):
                matching_rides.append(ride)
        return matching_rides

    try:
        matching = await asyncio.to_thread(_find_matches_in_db)
        return matching
    except Exception as e:
        print(f"!!! UNHANDLED EXCEPTION in /search: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@router.get("/my-rides", response_model=List[RideOut])
def get_my_rides(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns every ride published by the currently authenticated driver.
    """
    rides = db.query(Ride).filter(Ride.driver_id == current_user.id).all()
    return rides