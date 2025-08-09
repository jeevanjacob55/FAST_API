# app/api/bookings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Ride, Booking
from app.schemas import BookingCreate, BookingOut
from typing import Optional

router = APIRouter()

@router.post("/{ride_id}/book", response_model=BookingOut)
def book_ride(ride_id: int, payload: BookingCreate, db: Session = Depends(get_db)):
    """
    Book a seat on the ride. Decrements seats if available and returns booking.
    For now user_id comes from the payload (replace with auth in future).
    """
    user_id = payload.user_id or 1  # placeholder until auth is ready
    print(f"DEBUG: Book request received: ride_id={ride_id}, user_id={user_id}")

    # 1) Find the ride
    ride = db.query(Ride).filter_by(id=ride_id).first()
    if not ride:
        print(f"DEBUG: Ride not found for ride_id={ride_id}. Check if ride_id is valid and exists in the database.")
        raise HTTPException(status_code=404, detail=f"Ride with id {ride_id} not found")

    print(f"DEBUG: Ride found: id={ride.id}, seats={ride.seats}")

    if ride.seats <= 0:
        print("DEBUG: No seats available for ride", ride_id)
        raise HTTPException(status_code=400, detail="No seats available")

    # Optional: prevent duplicate booking by same user
    existing = db.query(Booking).filter_by(ride_id=ride_id, user_id=user_id, status="confirmed").first()
    if existing:
        print(f"DEBUG: User {user_id} already has booking {existing.id} for ride {ride_id}")
        raise HTTPException(status_code=400, detail="User already booked this ride")

    try:
        # Use a transaction block. In SQLite this is still limited, but it's better than nothing.
        try:
            print("DEBUG: Decrementing seats and creating booking...")
            ride.seats = ride.seats - 1
            booking = Booking(
                ride_id=ride_id,
                user_id=user_id,
                status="confirmed"
            )
            db.add(booking)
            db.commit()
            db.refresh(booking)
            db.refresh(ride)
            print(f"DEBUG: Booking committed: id={booking.id}, ride.seats now={ride.seats}")
        except Exception as e:
            db.rollback()
            print("DEBUG: Exception during commit:", str(e))
            raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")

    except Exception as e:
        print("DEBUG: Exception while booking:", str(e))
        # If something goes wrong, return 500 and let caller retry
        raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")

    return booking

#cancel the route, the varialbes are passed in url format
@router.post("/{ride_id}/cancel", response_model=BookingOut)
def cancel_booking(ride_id: int, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Cancel a confirmed booking for a ride and increment seats.
    For now user_id comes from query param (replace with auth in future).
    """
    user_id = user_id or 1  # placeholder until auth is ready
    print(f"DEBUG: Cancel request received: ride_id={ride_id}, user_id={user_id}")

    booking = db.query(Booking).filter_by(ride_id=ride_id, user_id=user_id, status="confirmed").first()
    if not booking:
        print(f"DEBUG: No confirmed booking found for user {user_id} on ride {ride_id}")
        raise HTTPException(status_code=404, detail="Booking not found")

    ride = db.query(Ride).filter_by(id=ride_id).first()
    if not ride:
        print(f"DEBUG: Ride not found for ride_id={ride_id}")
        raise HTTPException(status_code=404, detail="Ride not found")

    try:
        print("DEBUG: Cancelling booking and incrementing seats...")
        booking.status = "cancelled"
        ride.seats = ride.seats + 1
        db.commit()
        db.refresh(booking)
        db.refresh(ride)
        print(f"DEBUG: Booking cancelled: id={booking.id}, ride.seats now={ride.seats}")
    except Exception as e:
        db.rollback()
        print("DEBUG: Exception during cancellation:", str(e))
        raise HTTPException(status_code=500, detail=f"Cancellation failed: {str(e)}")

    return booking
#cancel the booking for the ride
# Note: This code assumes that the ride_id and user_id are valid and exist in the database.