# app/schemas.py
from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional
# Auth
class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Rides
# class RideCreate(BaseModel):
#     leaving_from: str
#     going_to: str
#     seats: int

class RideCreate(BaseModel):
    driver_username: str
    leaving_from: str
    going_to: str
    date: Optional[date]
    time: Optional[time]
    seats: int
    polyline: Optional[str] = None
class RideOut(BaseModel):
    id: int
    leaving_from: str
    going_to: str
    seats: int
    driver_id: int
    polyline: str | None = None  # so frontend can draw the route

    class Config:
        orm_mode = True

class RideSearch(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    tolerance: float = 5.0 # km tolerance for matching

#BOOKING SCHEMAS
class BookingCreate(BaseModel):
    # Ideally user_id is derived from auth; for now optional (defaults to 1)
    user_id: Optional[int] = None

class BookingOut(BaseModel):
    id: int
    ride_id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True