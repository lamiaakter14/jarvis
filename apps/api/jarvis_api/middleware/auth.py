"""JWT authentication middleware and utilities for the API."""

import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# JWT Configuration - Load from environment variables
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable must be set")

ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))

security = HTTPBearer()


class TokenData(BaseModel):
    """Token payload data."""

    user_id: str
    username: str
    role: str = "user"
    exp: datetime


class TokenPair(BaseModel):
    """Access and refresh token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token.

    Args:
        data: Payload data to encode
        expires_delta: Token expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token.

    Args:
        data: Payload data to encode
        expires_delta: Token expiration time

    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_token_pair(user_id: str, username: str, role: str = "user") -> TokenPair:
    """Create access and refresh token pair.

    Args:
        user_id: User identifier
        username: Username
        role: User role

    Returns:
        TokenPair with access and refresh tokens
    """
    token_data = {"user_id": user_id, "username": username, "role": role}

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenPair(access_token=access_token, refresh_token=refresh_token)


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> TokenData:
    """Get current authenticated user from JWT token.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        TokenData with user information

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    payload = decode_token(token)

    user_id = payload.get("user_id")
    username = payload.get("username")
    role = payload.get("role", "user")
    exp = payload.get("exp")

    if user_id is None or username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenData(user_id=user_id, username=username, role=role, exp=datetime.fromtimestamp(exp))


async def require_admin(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Require admin role for endpoint access.

    Args:
        current_user: Current authenticated user

    Returns:
        TokenData if user is admin

    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


def verify_refresh_token(token: str) -> Dict[str, Any]:
    """Verify and decode refresh token.

    Args:
        token: Refresh token to verify

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or not a refresh token
    """
    payload = decode_token(token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401, detail="Invalid token type", headers={"WWW-Authenticate": "Bearer"}
        )

    return payload
