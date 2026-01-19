from fastapi import FastAPI
from app.database.db import engine, Base
from app.routers import auth, users, admin,otp_auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication and Authorization API USING FASTAPI & POSTGRESQL WITH ROLES & PERMISSIONS")

app.include_router(auth.router)
app.include_router(otp_auth.router)
app.include_router(users.router)
app.include_router(admin.router)
