import hashlib

def hash_password(password: str) -> str:
    # simple SHA256 hash
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed
