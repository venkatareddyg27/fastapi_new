from sqlalchemy import Column, Integer, String, DateTime,Boolean
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, nullable=False)
    permissions = Column(String, nullable=True)

    otp = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    otp_attempts = Column(Integer, default=0)
    email_verified = Column(Boolean, default=False)


