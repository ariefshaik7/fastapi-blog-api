from datetime import timedelta, datetime, timezone
from app.schemas import token_schema
from app.core.config import settings
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_db
from app.models.models import User
from sqlalchemy import select


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict):
    """
    Generate a new JWT access token
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verifies the JWT token.
    Returns the token's payload (data) if successful.
    """

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = token_schema.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """
    A dependency that can be added to any endpoint
    to get the currently authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    query = select(User).where(User.id == token_data.id)

    user = await db.scalar(query)

    if user is None:
        raise credentials_exception

    return user
