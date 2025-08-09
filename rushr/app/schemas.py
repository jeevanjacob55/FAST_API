from pydantic import BaseModel, EmailStr
from datetime import date, time, datetime
from typing import Optional

# --- Auth Schemas ---
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    contact_number: str
    aadhaar_number: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- User Schemas ---
class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    contact_number: str
    role: str
    class Config:
        from_attributes = True

class DriverRegister(BaseModel):
    driving_license: str
    vehicle_number_plate: str

# --- Ride Schemas ---
class RideCreate(BaseModel):
    leaving_from: str
    going_to: str
    seats: int
    # Removed other fields to match your latest auth.py logic

class RideOut(BaseModel):
    id: int
    leaving_from: str
    going_to: str
    seats: int
    driver_id: int
    polyline: str | None = None
    class Config:
        from_attributes = True # ✅ FIXED: Changed orm_mode to from_attributes

# class RideSearch(BaseModel):
#     start_lat: float
#     start_lon: float
#     end_lat: float
#     end_lon: float
#     tolerance: float = 5.0

# ... other schemas

# CHANGE THIS SCHEMA
class RideSearch(BaseModel):
    leaving_from: str
    going_to: str
    # tolerance: float = 5.0 # This can be a query parameter instead

# --- Booking Schemas ---
class BookingCreate(BaseModel):
    user_id: Optional[int] = None

class BookingOut(BaseModel):
    id: int
    ride_id: int
    user_id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True # ✅ FIXED: Changed orm_mode to from_attributes