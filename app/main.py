from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database.db import engine, SessionLocal, Base
from app.database.models import User
from app.core.security import hash_password
from app.routers import auth, otp_auth, users, admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication and Authorization API USING FASTAPI & POSTGRESQL WITH ROLES & PERMISSIONS")

app.include_router(auth.router)
app.include_router(otp_auth.router)
app.include_router(users.router)
app.include_router(admin.router)

def create_default_superadmin():
    db: Session = SessionLocal()
    try:
        superadmin = db.query(User).filter(User.role == "superadmin").first()

        if not superadmin:
            admin = User(
                username="superadmin",
                email="superadmin@gmail.com",
                hashed_password=hash_password("superadmin@123"),
                role="superadmin",
                permissions="*",
                email_verified=True
            )
            db.add(admin)
            db.commit()
            print(" Default superadmin created")
        else:
            print(" Superadmin already exists")
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    create_default_superadmin()
    print(" Application has started")