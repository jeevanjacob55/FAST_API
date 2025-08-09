# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate, TokenResponse
from app.models import User
from app.core.security import hash_password, verify_password, create_token
from app.db import get_db
import logging
router = APIRouter()
logger = logging.getLogger("auth")
logger = logging.getLogger("auth")

@router.post("/signup", response_model=TokenResponse)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    logger.debug(f"Signup attempt for username: {data.username}")
    existing_user = db.query(User).filter_by(username=data.username).first()
    if existing_user:
        logger.debug(f"Username '{data.username}' is already taken.")
        raise HTTPException(status_code=400, detail="Username taken")
    hashed = hash_password(data.password)
    logger.debug(f"Password hashed for username: {data.username}")
    user = User(username=data.username, password=hashed)
    db.add(user)
    db.commit()
    logger.debug(f"User '{data.username}' created successfully.")
    token = create_token({"sub": user.username})
    logger.debug(f"Token generated for username: {data.username}")
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_token({"sub": user.username}))

