from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Make sure to import all your modules
from .db import engine
from .models import Base
from .api import auth, rides, bookings 

# This creates the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rushr API"
)

# --- This is the correct placement for CORS middleware ---
# It must come before you include your routers.
origins = [
    "http://localhost:5173", # For Vite
    "http://localhost:3000", # For Create React App
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------------------------------------------------

# Include all your API routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(rides.router, prefix="/rides", tags=["Rides"])
app.include_router(bookings.router, prefix="/rides", tags=["Bookings"]) # Assuming bookings are also under /rides

# Define the root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {"status": "API is running"}