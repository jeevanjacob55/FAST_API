import random
import datetime
import asyncio
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

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user in a non-blocking way.
    """
    def _check_user_in_db():
        return db.query(User).filter(
            or_(
                User.email == data.email,
                User.contact_number == data.contact_number,
                User.aadhaar_number == data.aadhaar_number
            )
        ).first()

    existing_user = await asyncio.to_thread(_check_user_in_db)

    if existing_user:
        if existing_user.email == data.email:
            detail = "Email is already registered."
        elif existing_user.contact_number == data.contact_number:
            detail = "Contact number is already registered."
        else:
            detail = "Aadhaar number is already registered."
        raise HTTPException(status_code=400, detail=detail)

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

    def _commit_user_to_db():
        db.add(new_user)
        db.commit()

    await asyncio.to_thread(_commit_user_to_db)

    print(f"Rushr OTP for {data.email}: {otp}")
    return {"message": f"OTP sent to {data.contact_number}. Please verify to complete signup."}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
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
        status_code = 404 if "not found" in error_detail else 400
        raise HTTPException(status_code=status_code, detail=error_detail)

    token = create_token({"sub": user.email})
    return TokenResponse(access_token=token)


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