from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Make sure this is imported

from .db import engine
from .models import Base
from .api import auth, rides

# This creates the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rushr API"
)

# --- This is the crucial section ---
# It must come before you include your routers.
origins = [
    "http://localhost:5173", # For Vite
    "http://localhost:3000", # For Create React App
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # List of allowed origins
    allow_credentials=True,    # Allows cookies
    allow_methods=["*"],         # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],         # Allows all headers
)
# ------------------------------------

# Include your API routers AFTER the middleware
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(rides.router, prefix="/rides", tags=["Rides"])

@app.get("/")
def read_root():
    return {"status": "API is running"}