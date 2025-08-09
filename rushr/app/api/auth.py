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
# inside signup()


# inside login()
 

@router.post("/signup", response_model=TokenResponse)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    logger.debug(f"Signup attempt for username: {data.username}")
    if not hasattr(data, "username") or not hasattr(data, "password"):
        logger.error("UserCreate schema missing username or password.")
        raise HTTPException(status_code=422, detail="Missing username or password")
    existing_user = db.query(User).filter_by(username=data.username).first()
    if existing_user:
        logger.debug(f"Username '{data.username}' is already taken.")
        raise HTTPException(status_code=400, detail="Username taken")
    hashed = hash_password(data.password)
    logger.debug(f"Password hashed for username: {data.username}")
    user = User(username=data.username, password=hashed)
    db.add(user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error during signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    db.refresh(user)
    logger.debug(f"User '{data.username}' created successfully.")
    token = create_token({"sub": user.username, "user_id": user.id})
    logger.debug(f"Token generated for username: {data.username}")
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=data.username).first()
    if not user or not verify_password(data.password, user.password):
        logger.debug(f"Login failed for username: {data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.username, "user_id": user.id})
    logger.debug(f"Login successful for username: {data.username}")
    return TokenResponse(access_token=token)

