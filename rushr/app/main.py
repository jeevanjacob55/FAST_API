# app/main.py

from fastapi import FastAPI
from .db import engine # Import engine and Base from db.py
from .models import Base
from .api import auth, rides
from app.api import bookings

# This is where the table creation logic now lives
# It connects the engine to the metadata from Base
Base.metadata.create_all(bind=engine)

# Create the main FastAPI app instance
app = FastAPI(
    title="Carpooling API"
)
# 1️⃣  Auth endpoints
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# 2️⃣  Ride CRUD endpoints
app.include_router(rides.router, prefix="/rides", tags=["Rides"])

# 3️⃣  Booking endpoints (book / cancel) live under /rides
app.include_router(bookings.router, prefix="/rides", tags=["Rides"])

# This decorator tells FastAPI to run this function once, on startup
# @app.on_event("startup")
# def on_startup():
#     """
#     Creates database tables if they don't exist.
#     """
#     print("Creating database tables...")
#     create_tables()
#     print("Tables created.")


@app.get("/", tags=["Root"])
def read_root():
    return {"status": "API is running"}


