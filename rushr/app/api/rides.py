# app/api/rides.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import RideCreate, RideOut, RideSearch
from app.models import Ride
from app.utils.google_maps import fetch_route_polyline #fetches polyline from Google Maps
import polyline
from haversine import haversine, Unit

router = APIRouter()

# --- Helper Function for Route Matching ---
def is_point_near_polyline(point: tuple, route_polyline: str, max_distance_km: float = 2.0) -> bool:
    """Checks if a lat/lon point is within a given distance of a polyline."""
    try:
        decoded_route = polyline.decode(route_polyline)
    except:
        return False # Handle invalid polylines
    
    for i in range(len(decoded_route) - 1):
        p1 = decoded_route[i]
        p2 = decoded_route[i+1]
        
        # This is a simplified check. For real accuracy, you'd calculate the
        # perpendicular distance from the point to the line segment.
        # For now, checking against the segment's start point is a good approximation.
        if haversine(point, p1, unit=Unit.KILOMETERS) <= max_distance_km:
            return True
            
    # Check the last point
    if decoded_route and haversine(point, decoded_route[-1], unit=Unit.KILOMETERS) <= max_distance_km:
        return True

    return False

@router.post("/publish", response_model=RideOut)
def publish_ride(ride: RideCreate, db: Session = Depends(get_db)): #, current_user: User = Depends(get_current_user)):
    try:
        # NOTE: You'd get the real polyline from a service like Google Maps API
        # polyline = fetch_route_polyline(ride.leaving_from, ride.going_to)
        # For this example, let's assume a dummy polyline is passed in the request
        if not ride.polyline:
            raise HTTPException(status_code=400, detail="Polyline is required for publishing a ride.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_ride = Ride(
        leaving_from=ride.leaving_from,
        going_to=ride.going_to,
        seats=ride.seats,
        # driver_id=current_user.id,  # TODO: Use real authenticated user
        driver_id=1,
        polyline=ride.polyline,
    )
    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
    return new_ride


@router.post("/search", response_model=list[RideOut])
def search_rides(data: RideSearch, db: Session = Depends(get_db)):
    """
    Searches for rides that pass near the passenger's start and end points.
    """
    # For efficiency, you might pre-filter rides in the DB, e.g., by date or a coarse bounding box.
    # For now, we fetch all active rides.
    all_rides = db.query(Ride).filter(Ride.seats > 0).all()

    matching_rides = []
    passenger_start = (data.start_lat, data.start_lon)
    passenger_end = (data.end_lat, data.end_lon)

    for ride in all_rides:
        if not ride.polyline:
            continue
            
        # 1. Check if the ride's route passes near the passenger's start point
        is_start_close = is_point_near_polyline(passenger_start, ride.polyline)

        # 2. Check if the ride's route passes near the passenger's end point
        if is_start_close:
            is_end_close = is_point_near_polyline(passenger_end, ride.polyline)
            if is_end_close:
                # TODO: A crucial third step is to verify that the pickup point on the
                # route comes BEFORE the drop-off point. This requires more complex polyline analysis.
                matching_rides.append(ride)

    return matching_rides
