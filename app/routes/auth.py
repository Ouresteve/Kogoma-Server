from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import create_user, authenticate_user
from app.config.database import users_collection
import jwt
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

JWT_SECRET = os.getenv("JWT_SECRET")


@router.post("/register")
async def register(user: UserCreate):
    existing = await users_collection.find_one({"email": user.email.lower().strip()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    await create_user(user.dict())
    return {
        "message": "Account created. Await admin approval."
    }

@router.post("/login")
async def login(user: UserLogin):
    token = await authenticate_user(user.email, user.password)
    
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if token == "NOT_APPROVED":
        raise HTTPException(status_code=403, detail="Account awaiting approval")

    return {
        "access_token": token,
        "token_type": "bearer"
    }





