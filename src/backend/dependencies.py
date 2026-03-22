import os

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")
ALGORITHM = "HS256"

# auto_error=False so we can return 401 (not FastAPI's default 403) when missing
_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_instructor(user: dict = Depends(get_current_user)) -> dict:
    if user.get("role") != "instructor":
        raise HTTPException(status_code=403, detail="Instructor role required")
    return user
