from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.models import User
from app.core.security import hash_password
from app.core.role_permissions import ROLE_PERMISSIONS

router = APIRouter(prefix="/auth", tags=["User Registration"])


@router.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("user"),
    db: Session = Depends(get_db)
):
    # Check if user already exists
    if db.query(User).filter(
        (User.username == username) |
        (User.email == email)
    ).first():
        raise HTTPException(status_code=400, detail="User already exists")

    # Validate role
    if role not in ROLE_PERMISSIONS:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=role,
        permissions=",".join(ROLE_PERMISSIONS[role])
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}
