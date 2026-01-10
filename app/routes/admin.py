from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.utils.security import hash_password
from app.middleware.auth import get_current_user
from pymongo import ASCENDING
from bson import ObjectId
from app.config.database import db
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.kogoma_db

router = APIRouter(prefix="/admin", tags=["admin"])

# Get all users (for approval)
@router.get("/users", response_model=list[UserOut])
async def get_all_users(current_user=Depends(get_current_user)):
    if current_user is None or current_user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        cursor = db.users.find().sort("created_at", ASCENDING)
        users = await cursor.to_list(None)  # Await and convert to list (None = no limit)
        for user in users:
            user["_id"] = str(user["_id"])

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return users


@router.put("/users/{user_id}/approve", response_model=UserOut)
async def approve_user(user_id: str, update: UserUpdate, current_user=Depends(get_current_user)):
    if current_user is None or current_user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": True, "role": update.role}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    user["_id"] = str(user["_id"])

    return user