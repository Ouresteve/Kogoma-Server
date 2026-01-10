from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    role: str  # e.g., "user", "staff", "admin"

class UserOut(BaseModel):
    id: str = Field(alias="_id")  # Maps DB '_id' to 'id', auto-converts ObjectId to str
    name: str
    email: str
    role: str
    approved: bool = Field(alias="is_active")  # Maps 'is_active' to 'approved'
    # Add other fields like 'created_at' if in DB and needed
    # created_at: Optional[datetime] = None  # Make optional if not alway

class Config:
    populate_by_name = True  # Enables alias mapping
    from_attributes = True
    json_encoders = {ObjectId: str}  # Auto-converts ObjectId to str for JSON
    exclude = {"password"}  # Automatically exclude sensitive fields
    json_encoders = {
            object: str
        }