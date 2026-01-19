from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.role_permissions import ROLE_PERMISSIONS
from app.database.models import User
from app.database.dependencies import get_db
from app.schemas.users import UserCreate, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["User Registration"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(
        (User.username == user.username) |
        (User.email == user.email)
    ).first():
        raise HTTPException(status_code=400, detail="User already exists")

    permissions = ROLE_PERMISSIONS.get(user.role, [])

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
        permissions=",".join(permissions)
    )

    db.add(db_user)
    db.commit()

    return {"message": "User created successfully"}

