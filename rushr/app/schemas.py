# app/schemas.py
from pydantic import BaseModel

# Auth
class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Rides
class RideCreate(BaseModel):
    leaving_from: str
    going_to: str
    seats: int
    polyline: str

class RideOut(BaseModel):
    id: int
    leaving_from: str
    going_to: str
    seats: int
    driver_id: int
    polyline: str  # add this
    class Config:
        orm_mode = True

class RideSearch(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
