import random
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_otp():
    return str(random.randint(100000, 999999))

def hash_otp(otp: str):
    return pwd_context.hash(otp)

def verify_otp(plain_otp, hashed_otp):
    return pwd_context.verify(plain_otp, hashed_otp)

def otp_expiry(minutes=5):
    return datetime.utcnow() + timedelta(minutes=minutes)
