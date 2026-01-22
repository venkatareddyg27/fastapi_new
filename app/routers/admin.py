from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.role_permissions import ROLE_PERMISSIONS, ALLOWED_ROLES
from app.database.models import User
from app.database.dependencies import get_db
from app.schemas.users import UserCreate, UserResponse
from app.core.permissions import (
    USER_CREATE, USER_READ, USER_UPDATE, USER_DELETE
)
from app.routers.permissions import permission_required
from app.core.security import hash_password

router = APIRouter(prefix="/admin", tags=["Admin or SuperAdmin only"])


# CREATE → user / admin / superadmin
@router.post(
    "/",
    response_model=UserResponse,
    dependencies=[Depends(permission_required(USER_CREATE))]
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
        permissions=""  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#  READ → admin / superadmin
@router.get(
    "/",
    response_model=list[UserResponse],
    dependencies=[Depends(permission_required(USER_READ))]
)
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


#  UPDATE → admin / superadmin
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(permission_required(USER_UPDATE))]
)
def update_user_role(user_id: int, role: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role
    db.commit()
    db.refresh(user)
    return user


# DELETE → superadmin ONLY
@router.delete(
    "/{user_id}",
    dependencies=[Depends(permission_required(USER_DELETE))]
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

# 🔁 CHANGE USER ROLE (admin / superadmin)
@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
    dependencies=[Depends(permission_required(USER_UPDATE))]
)
def change_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db)
):
    # Validate role
    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update role + permissions
    user.role = role
    user.permissions = ",".join(ROLE_PERMISSIONS.get(role, []))

    db.commit()
    db.refresh(user)
    return user
