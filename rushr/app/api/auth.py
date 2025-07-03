# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate, TokenResponse
from app.models import User
from app.core.security import hash_password, verify_password, create_token
from app.db import get_db

router = APIRouter()

@router.post("/signup", response_model=TokenResponse)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=data.username).first():
        raise HTTPException(status_code=400, detail="Username taken")
    hashed = hash_password(data.password)
    user = User(username=data.username, password=hashed)
    db.add(user)
    db.commit()
    return TokenResponse(access_token=create_token({"sub": user.username}))

@router.post("/login", response_model=TokenResponse)
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_token({"sub": user.username}))
