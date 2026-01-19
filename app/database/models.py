from sqlalchemy import Column, Integer, String, DateTime
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    hashed_password = Column(String, nullable=True)
    role = Column(String, default="user")
    permissions = Column(String, default="")

    otp = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
