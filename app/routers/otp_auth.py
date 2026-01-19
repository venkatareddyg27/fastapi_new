from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.dependencies import get_db
from app.database.models import User
from app.core.otp import generate_otp, hash_otp, verify_otp, otp_expiry
from app.core.email import send_otp_email
from app.core.security import create_access_token
from app.schemas.otp import OTPRequest, OTPVerify

router = APIRouter(prefix="/otpauth", tags=["OTP Verification"])


@router.post("/request-otp")
def request_otp(data: OTPRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    user.otp = hash_otp(otp)
    user.otp_expiry = otp_expiry()

    db.commit()
    send_otp_email(user.email, otp)

    return {"message": "OTP sent to email"}


@router.post("/verify-otp")
def verify_otp_login(data: OTPVerify, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not user.otp:
        raise HTTPException(status_code=400, detail="Invalid request")

    if datetime.utcnow() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="OTP expired")

    if not verify_otp(data.otp, user.otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")

    user.otp = None
    user.otp_expiry = None
    db.commit()

    token = create_access_token({
        "sub": user.username,
        "role": user.role,
        "permissions": user.permissions.split(",") if user.permissions else []
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
