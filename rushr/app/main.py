# app/main.py
from fastapi import FastAPI
from app.api import auth, rides
from app.db import create_tables

app = FastAPI()
create_tables()
@app.get("/")
def read_root():
    return {"status": "Rushr backend is running"}
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(rides.router, prefix="/rides", tags=["Rides"])

