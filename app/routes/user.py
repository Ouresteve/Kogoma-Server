from fastapi import APIRouter , Depends, HTTPException
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.middleware.auth import get_current_user
from pymongo import ASCENDING
from bson import ObjectId
from app.config.database import db
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.kogoma_db

router = APIRouter(prefix="/user", tags=["user"])

#Get current user profile
@router.get("/me", response_model=UserOut)
async def get_current_user_profile(current_user=Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user= await db.users.find_one({"_id": current_user["_id"]})
    user["_id"] = str(user["_id"]) # converts objectId to string for Json serialization
    return user