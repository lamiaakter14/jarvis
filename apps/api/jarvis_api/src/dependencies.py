"""FastAPI dependencies."""
from fastapi import Depends
from sqlalchemy.orm import Session
from .config.database import get_db
from .middleware.auth import get_current_user, HTTPAuthorizationCredentials, security


async def get_current_user_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Dependency to get current authenticated user."""
    return await get_current_user(credentials)


def get_db_dependency() -> Session:
    """Dependency to get database session."""
    return Depends(get_db)
