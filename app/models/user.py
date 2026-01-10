from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str]
    name: str
    email: EmailStr
    password: str 
    role: str = "user"          # user, admin, staff, pharmacist
    is_active: bool = False     # approved or not
    created_at: datetime = datetime.utcnow()
