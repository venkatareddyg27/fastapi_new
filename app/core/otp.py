import random
from datetime import datetime, timedelta
from passlib.context import CryptContext
from zoneinfo import ZoneInfo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

IST = ZoneInfo("Asia/Kolkata")


def generate_otp():
    return str(random.randint(100000, 999999))

def hash_otp(otp: str):
    return pwd_context.hash(otp)

def verify_otp(plain_otp, hashed_otp):
    return pwd_context.verify(plain_otp, hashed_otp)

def otp_expiry(minutes: int = 5):
    return datetime.now(IST) + timedelta(minutes=minutes)
