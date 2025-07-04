# app/api/rides.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import RideCreate, RideOut
from app.models import Ride
from app.utils.google_maps import fetch_route_polyline #fetches polyline from Google Maps


router = APIRouter()

@router.post("/publish", response_model=schemas.RideOut)
def publish_ride(ride: schemas.RideCreate, db: Session = Depends(get_db)):
    try:
        polyline = fetch_route_polyline(ride.leaving_from, ride.going_to)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_ride = Ride(
        leaving_from=ride.leaving_from,
        going_to=ride.going_to,
        seats=ride.seats,
        driver_id=1,  # Placeholder until real auth
        polyline=polyline
    )

    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
    return new_ride


@router.post("/search", response_model=list[RideOut])
def search_rides(data: RideCreate, db: Session = Depends(get_db)):
    rides = db.query(Ride).filter(
        Ride.leaving_from.ilike(data.leaving_from),
        Ride.going_to.ilike(data.going_to)
    ).all()
    return rides
