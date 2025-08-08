# app/api/rides.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import RideCreate, RideOut, RideSearch
from app.models import Ride
from app.utils.google_maps import fetch_route_polyline #fetches polyline from Google Maps
import polyline
from haversine import haversine, Unit
from app.utils.route_matching import route_matches
from typing import List
router = APIRouter()

@router.post("/publish/", response_model=RideOut)
def publish_ride(ride: RideCreate, db: Session = Depends(get_db)):
    print("DEBUG: Received publish request:", ride.dict())

    try:
        # ✅ Generate polyline using Google Maps Directions API
        print(f"DEBUG: Fetching polyline from '{ride.leaving_from}' to '{ride.going_to}'...")
        polyline = fetch_route_polyline(ride.leaving_from, ride.going_to)
        print("DEBUG: Polyline received:", polyline)

        if not polyline:
            print("DEBUG: No polyline generated.")
            raise HTTPException(status_code=400, detail="Could not generate route polyline.")
    except Exception as e:
        print("DEBUG: Exception while generating polyline:", str(e))
        raise HTTPException(status_code=400, detail=f"Polyline generation failed: {str(e)}")

    try:
        print("DEBUG: Creating Ride object...")
        new_ride = Ride(
            leaving_from=ride.leaving_from,
            going_to=ride.going_to,
            seats=ride.seats,
            driver_id=1,  # 🔒 Replace with real user ID when auth is ready
            polyline=polyline,
        )

        print("DEBUG: Adding ride to DB session...")
        db.add(new_ride)

        print("DEBUG: Committing transaction...")
        db.commit()

        print("DEBUG: Refreshing ride object...")
        db.refresh(new_ride)

        print("DEBUG: Ride published successfully:", new_ride)
    except Exception as e:
        print("DEBUG: Exception while saving ride:", str(e))
        raise HTTPException(status_code=500, detail=f"Error saving ride: {str(e)}")

    return new_ride


@router.post("/search", response_model=List[RideOut])
def search_rides(search: RideSearch, db: Session = Depends(get_db), tolerance_km: float = 2.0):
    """
    Return all rides whose stored polyline passes near both the start and end points,
    and where the pickup point is ordered before the drop-off on the route.
    """
    passenger_start = (search.start_lat, search.start_lon)
    passenger_end   = (search.end_lat, search.end_lon)

    # Basic DB prefilter: only consider rides that have a polyline and available seats
    rides = db.query(Ride).filter(Ride.polyline != None, Ride.seats > 0).all()

    matching = []
    for ride in rides:
        try:
            if route_matches(passenger_start, passenger_end, ride.polyline, tolerance_km=tolerance_km):
                matching.append(ride)
        except Exception as e:
            print(f"DEBUG: error checking ride {ride.id}: {e}")
            # continue checking other rides rather than failing the whole request

    return matching