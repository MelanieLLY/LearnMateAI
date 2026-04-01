"""FastAPI dependency functions for authentication and authorisation.

All AI agent calls and protected routes must flow through these dependencies
to guarantee that only authenticated users with the correct role can proceed.
"""

import os

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

SECRET_KEY: str = os.environ.get("SECRET_KEY", "changeme")
ALGORITHM: str = "HS256"

# auto_error=False lets us raise HTTP 401 ourselves instead of FastAPI's
# default 403 when the Authorization header is absent.
_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    """Decode the Bearer JWT and return its payload as a plain dict.

    Checks the 'access_token' cookie first, then falls back to the Authorization header.

    Args:
        request: The initial FastAPI Request object containing cookies.
        credentials: The parsed Authorization header, or ``None`` if absent.

    Returns:
        The decoded JWT claims dict (e.g. ``{"sub": "1", "role": "instructor"}``).

    Raises:
        HTTPException: 401 if the header/cookie is missing or the token is invalid.
    """
    token = None
    
    # 1. Try to get token from HttpOnly Cookie
    cookie_token = request.cookies.get("access_token")
    if cookie_token and cookie_token.startswith("Bearer "):
        token = cookie_token[7:]
    
    # 2. Try to get token from Authorization Header
    if not token and credentials:
        token = credentials.credentials
        
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
