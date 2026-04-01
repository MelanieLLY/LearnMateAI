import os
from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt

SECRET_KEY: str = os.environ.get("SECRET_KEY", "changeme")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days for convenience

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # bcrypt.checkpw requires bytes
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    # bcrypt.hashpw returns bytes, we decode to string for db storage
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
