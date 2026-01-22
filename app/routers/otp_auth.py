from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.dependencies import get_db
from app.database.models import User
from app.core.otp import generate_otp, hash_otp, verify_otp, otp_expiry
from app.core.security import verify_password, create_access_token
from app.core.email import send_otp_email
from zoneinfo import ZoneInfo
IST = ZoneInfo("Asia/Kolkata")
router = APIRouter(prefix="/otp", tags=["Otp generation and login to generate token"])

@router.post("/request-otp")
def request_otp(
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp = generate_otp()
    user.otp = hash_otp(otp)
    user.otp_expiry = otp_expiry()
    db.commit()
    db.refresh(user)
    send_otp_email(user.email, otp)
    return {"message": "OTP sent to registered email"}

@router.post("/login")
def login(
    email: str = Form(...),
    password: str | None = Form(None),
    otp: str | None = Form(None),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not password and not otp:
        raise HTTPException(
            status_code=400,
            detail="Provide either password or OTP"
        )

    # PASSWORD LOGIN
    if password:
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password")

        # reset OTP attempts on successful password login
        user.otp_attempts = 0
        db.commit()

    #  OTP LOGIN
    elif otp:
        # BLOCK AFTER 3 ATTEMPTS
        if user.otp_attempts >= 3:
            raise HTTPException(
                status_code=403,
                detail="Too many OTP attempts. Please request a new OTP."
            )

        if not user.otp or not user.otp_expiry:
            raise HTTPException(status_code=400, detail="OTP not requested")

        if datetime.utcnow() > user.otp_expiry:
            raise HTTPException(status_code=400, detail="OTP expired")

        #  WRONG OTP
        if not verify_otp(otp, user.otp):
            user.otp_attempts += 1
            db.commit()  

            raise HTTPException(
                status_code=401,
                detail=f"Invalid OTP. Attempts: {user.otp_attempts}"
            )

        #  OTP SUCCESS
        user.otp_attempts = 0
        db.commit()

    # JWT TOKEN
    token = create_access_token({
        "sub": user.email,
        "role": user.role,
        "permissions": user.permissions.split(",") if user.permissions else []
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
