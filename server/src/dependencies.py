"""FastAPI dependency functions for authentication and authorisation.

All AI agent calls and protected routes must flow through these dependencies
to guarantee that only authenticated users with the correct role can proceed.
"""

import os

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

SECRET_KEY: str = os.environ.get("SECRET_KEY", "changeme")
ALGORITHM: str = "HS256"

# auto_error=False lets us raise HTTP 401 ourselves instead of FastAPI's
# default 403 when the Authorization header is absent.
_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    """Decode the Bearer JWT and return its payload as a plain dict.

    Args:
        credentials: The parsed Authorization header, or ``None`` if absent.

    Returns:
        The decoded JWT claims dict (e.g. ``{"sub": "1", "role": "instructor"}``).

    Raises:
        HTTPException: 401 if the header is missing or the token is invalid.
    """
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_student(user: dict = Depends(get_current_user)) -> dict:
    """Extend ``get_current_user`` to enforce the student role.

    Args:
        user: The decoded JWT payload returned by ``get_current_user``.

    Returns:
        The same ``user`` dict, unchanged, if the role check passes.

    Raises:
        HTTPException: 403 if the authenticated user's role is not ``"student"``.
    """
    if user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Student role required")
    return user


def require_instructor(user: dict = Depends(get_current_user)) -> dict:
    """Extend ``get_current_user`` to enforce the instructor role.

    Args:
        user: The decoded JWT payload returned by ``get_current_user``.

    Returns:
        The same ``user`` dict, unchanged, if the role check passes.

    Raises:
        HTTPException: 403 if the authenticated user's role is not ``"instructor"``.
    """
    if user.get("role") != "instructor":
        raise HTTPException(status_code=403, detail="Instructor role required")
    return user
