from app.config.database import users_collection
from app.utils.security import hash_password, verify_password
from app.config.database import users_collection
from app.utils.security import verify_password
import jwt, os

JWT_SECRET = os.getenv("JWT_SECRET")

async def authenticate_user(email: str, password: str):
    email = email.lower().strip()
    user = await users_collection.find_one({"email": email})
    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

   # if not user.get('is_active',False):
    #    return "NOT_APPROVED"

    payload = {
        "sub": str(user["_id"]),
        "name": user["name"],
        "email": user["email"].lower().strip(),
        "role": user["role"]
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

async def create_user(user_data):
    user_data["password"] = hash_password(user_data["password"])
    user_data["role"] = "user"
    user_data["is_active"] = False

    await users_collection.insert_one(user_data)
    return True
