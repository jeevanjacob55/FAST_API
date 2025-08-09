# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from .db import Base # Make sure to import Base from your central db file
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    # ... (rest of the model is correct) ...
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    contact_number = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    aadhaar_number = Column(String, unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    otp = Column(String, nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)
    role = Column(String, default="rider")
    driving_license = Column(String, nullable=True, unique=True)
    vehicle_number_plate = Column(String, nullable=True, unique=True)

class Ride(Base):
    __tablename__ = "rides"
    # ... (rest of the model is correct) ...
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("users.id"))
    leaving_from = Column(String)
    going_to = Column(String)
    seats = Column(Integer)
    polyline = Column(String, nullable=True)

class Booking(Base):
    __tablename__ = "bookings"
    # ... (rest of the model is correct) ...
    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)