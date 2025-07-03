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

class RideOut(RideCreate):
    id: int
    driver_id: int
