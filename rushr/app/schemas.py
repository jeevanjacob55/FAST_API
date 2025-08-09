from pydantic import BaseModel, EmailStr
from datetime import date, time, datetime
from typing import Optional

# --- Auth Schemas ---
# app/schemas.py (Pydantic v2 style)
from pydantic import BaseModel, field_validator

class UserCreate(BaseModel):
    full_name: str
    email: str
    contact_number: str
    aadhaar_number: str
    password: str

    @field_validator("aadhaar_number")
    @classmethod
    def check_aadhaar(cls, v):
        from app.utils.validation import is_valid_aadhaar
        if not is_valid_aadhaar(v):
            raise ValueError("Invalid Aadhaar number")
        return v


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

class RideSearch(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    tolerance: float = 5.0

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