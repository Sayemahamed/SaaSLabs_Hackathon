from datetime import datetime, timedelta, timezone
from typing import Literal, Optional

import jwt

# Assuming API is a package/directory at the same level or in sys.path
from API.config import settings
from API.db import User, get_async_session
from fastapi import Depends, HTTPException, WebSocket, status
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, PyJWTError
from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# --- Constants ---
OAUTH2_SCHEME = OAuth2PasswordBearer(
    tokenUrl=f"/v1/auth/token"
)  # Use config for version
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
TOKEN_EXPIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)


# --- Password Utilities ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generates a hash for a given password."""
    return PWD_CONTEXT.hash(password)


# --- Token Utilities ---
def create_access_token(data: dict) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update(
        {"exp": expire, "iat": datetime.now(timezone.utc)}
    )  # Add issued at time
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# --- Authentication Service ---
class AuthService:
    """Handles authentication-related business logic."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session: AsyncSession = session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieves a user by their email address."""
        statement = select(User).where(
            User.email == email.lower()
        )  # Ensure lowercase comparison
        result = await self.session.exec(statement)
        return result.first()


# --- Dependency Functions ---
async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Dependency to get the current authenticated user from a token.
    Raises HTTPException if authentication fails.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True},  # Ensure expiration is checked
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
    except ExpiredSignatureError:
        raise TOKEN_EXPIRED_EXCEPTION
    except PyJWTError:  # Catches various JWT errors (invalid signature, format, etc.)
        raise CREDENTIALS_EXCEPTION

    # Fetch user from DB based on token subject (email)
    statement = select(User).where(User.email == username)
    result = await session.exec(statement)
    user = result.first()
    if user is None:
        # This case might indicate a deleted user whose token is still valid briefly
        raise CREDENTIALS_EXCEPTION
    return user


async def get_current_user_ws(
    token: str,  # Token is expected to be passed explicitly in WS context
    session: AsyncSession,  # Session needs to be provided to this function
) -> Optional[User] | Literal["expired"]:
    """
    Retrieves the current user for a WebSocket connection based on a token.

    Args:
        token: The JWT token string.
        session: The AsyncSession instance to use for database queries.

    Returns:
        The User object if authentication is successful.
        "expired" if the token has expired.
        None if the token is invalid or the user is not found.

    Note: This function expects the caller (WebSocket endpoint) to handle
          providing the token and the database session. It also returns
          special values ('expired', None) instead of raising exceptions
          to allow the WebSocket handler more control over the connection closure.
    """
    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True},
        )
        email: str | None = payload.get("sub")
        if not email:
            return None  # Token valid but no subject
    except ExpiredSignatureError:
        return "expired"
    except PyJWTError:
        return None  # Invalid token

    # Fetch user from DB
    result = await session.exec(select(User).where(User.email == email))
    user = result.first()
    # If user is None, the user associated with the valid token doesn't exist anymore
    return user
