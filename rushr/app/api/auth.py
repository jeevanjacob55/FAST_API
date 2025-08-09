# app/api/auth.py
import random# app/api/auth.py
import random
import datetime
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
<<<<<<< HEAD
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
=======

from app.db import get_db
from app.models import User
from app.schemas import UserCreate, LoginRequest, OTPVerify, TokenResponse
from app.core.security import hash_password, verify_password, create_token

router = APIRouter()

def _generate_otp() -> str:
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user in a non-blocking way.
    """
    # Define a synchronous function for the database check
    def _check_user_in_db():
        return db.query(User).filter(
            or_(
                User.email == data.email,
                User.contact_number == data.contact_number,
                User.aadhaar_number == data.aadhaar_number
            )
        ).first()

    # ✅ Run the blocking database query in a separate thread
    existing_user = await asyncio.to_thread(_check_user_in_db)

    if existing_user:
        if existing_user.email == data.email:
            detail = "Email is already registered."
        elif existing_user.contact_number == data.contact_number:
            detail = "Contact number is already registered."
        else:
            detail = "Aadhaar number is already registered."
        raise HTTPException(status_code=400, detail=detail)

    # ✅ Run the blocking CPU-bound hashing in a separate thread
    hashed_password = await asyncio.to_thread(hash_password, data.password)

    otp = _generate_otp()
    otp_expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    new_user = User(
        full_name=data.full_name,
        email=data.email,
        contact_number=data.contact_number,
        password=hashed_password,
        aadhaar_number=data.aadhaar_number,
        otp=otp,
        otp_expires_at=otp_expires_at,
        is_verified=False
    )

    # Define a synchronous function for the database commit
    def _commit_user_to_db():
        db.add(new_user)
        db.commit()

    # ✅ Run the blocking database write in a separate thread
    await asyncio.to_thread(_commit_user_to_db)

    print(f"Rushr OTP for {data.email}: {otp}")
    return {"message": f"OTP sent to {data.contact_number}. Please verify to complete signup."}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    # This function is simple enough that it may not block significantly,
    # but for consistency, we can make it fully async as well.
    def _verify_in_db():
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            return None, "User not found."
        if user.is_verified and user.otp is None:
            return None, "Account already verified. Please log in."
        if user.otp != data.otp or user.otp_expires_at < datetime.datetime.utcnow():
            return None, "Invalid or expired OTP."
        
        user.is_verified = True
        user.otp = None
        user.otp_expires_at = None
        db.commit()
        return user, None

    user, error_detail = await asyncio.to_thread(_verify_in_db)

    if error_detail:
        # Determine status code based on error
        status_code = 404 if "not found" in error_detail else 400
        raise HTTPException(status_code=status_code, detail=error_detail)

    token = create_token({"sub": user.email})
    return TokenResponse(access_token=token)

>>>>>>> ecd41bb7413d74a13b017129f1bb970baecf79da

@router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    def _login_check_in_db():
        return db.query(User).filter(User.email == data.email).first()

    user = await asyncio.to_thread(_login_check_in_db)

    is_password_valid = False
    if user:
        is_password_valid = await asyncio.to_thread(verify_password, data.password, user.password)

    if not user or not is_password_valid:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Account not verified. Please complete the signup process.")

    otp = _generate_otp()
    
    def _update_login_otp_in_db():
        user.otp = otp
        user.otp_expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        db.commit()

    await asyncio.to_thread(_update_login_otp_in_db)

    print(f"Rusha Login OTP for {data.email}: {otp}")
    return {"message": f"OTP sent to your registered contact number. Please use /verify-otp to log in."}
import datetime
import asyncio # Import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import UserCreate, LoginRequest, OTPVerify, TokenResponse
from app.core.security import hash_password, verify_password, create_token

router = APIRouter()

def _generate_otp() -> str:
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))

# ✅ CHANGE 1: Convert the function to be asynchronous with 'async def'
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, db: Session = Depends(get_db)):
    """
    Step 1 of Onboarding: Register a new user and send an OTP.
    This is now non-blocking.
    """
    # ✅ CHANGE 2: Combine database checks into a single, more efficient query.
    existing_user = db.query(User).filter(
        or_(
            User.email == data.email,
            User.contact_number == data.contact_number,
            User.aadhaar_number == data.aadhaar_number # ✅ CHANGE 3: Add check for Aadhaar to prevent crashes
        )
    ).first()

    if existing_user:
        if existing_user.email == data.email:
            detail = "Email is already registered."
        elif existing_user.contact_number == data.contact_number:
            detail = "Contact number is already registered."
        else:
            detail = "Aadhaar number is already registered."
        raise HTTPException(status_code=400, detail=detail)

    # ✅ CHANGE 4: Run the slow, CPU-bound hashing in a separate thread.
    hashed = await asyncio.to_thread(hash_password, data.password)

    otp = _generate_otp()
    otp_expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    new_user = User(
        full_name=data.full_name,
        email=data.email,
        contact_number=data.contact_number,
        password=hashed,
        aadhaar_number=data.aadhaar_number,
        otp=otp,
        otp_expires_at=otp_expires_at,
        is_verified=False
    )
    db.add(new_user)
    db.commit()

    print(f"Rusha OTP for {data.email}: {otp}")
    return {"message": f"OTP sent to {data.contact_number}. Please verify to complete signup."}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user.is_verified and user.otp is None:
         raise HTTPException(status_code=400, detail="Account already verified. Please log in.")

    if user.otp != data.otp or user.otp_expires_at < datetime.datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

    user.is_verified = True
    user.otp = None
    user.otp_expires_at = None
    db.commit()

    token = create_token({"sub": user.email})
    return TokenResponse(access_token=token)


@router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    # ✅ CHANGE 5: Also make password verification async to avoid blocking
    is_password_valid = await asyncio.to_thread(verify_password, data.password, user.password if user else "")

    if not user or not is_password_valid:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Account not verified. Please complete the signup process.")

    otp = _generate_otp()
    user.otp = otp
    user.otp_expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    db.commit()

    print(f"Rusha Login OTP for {data.email}: {otp}")
    return {"message": f"OTP sent to your registered contact number. Please use /verify-otp to log in."}