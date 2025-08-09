# app/main.py

from fastapi import FastAPI
from app.api import auth, rides
from app.db import create_tables
from app.api import bookings


# Create the main FastAPI app instance
app = FastAPI(
    title="Carpooling API"
)

# This decorator tells FastAPI to run this function once, on startup
@app.on_event("startup")
def on_startup():
    """
    Creates database tables if they don't exist.
    """
    print("Creating database tables...")
    create_tables()
    print("Tables created.")


# Include your routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# app.include_router(rides.router, prefix="/rides", tags=["Rides"])
app.include_router(rides.router)
# app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
app.include_router(bookings.router, prefix="/rides", tags=["Rides"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "API is running"}