# app/api/rides.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import RideCreate, RideOut
from app.models import Ride

router = APIRouter()

@router.post("/publish", response_model=RideOut)
def publish_ride(data: RideCreate, db: Session = Depends(get_db)):
    # In real case, get driver_id from auth token
    ride = Ride(**data.dict(), driver_id=1)
    db.add(ride)
    db.commit()
    db.refresh(ride)
    return ride

@router.post("/search", response_model=list[RideOut])
def search_rides(data: RideCreate, db: Session = Depends(get_db)):
    rides = db.query(Ride).filter(
        Ride.leaving_from.ilike(data.leaving_from),
        Ride.going_to.ilike(data.going_to)
    ).all()
    return rides
