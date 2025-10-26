from datetime import timedelta, datetime, timezone
from app.crud import user_crud
from app.schemas import token_schema
from app.core.config import settings
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from app.db.session import get_db
from app.models.models import User


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a new JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = token_schema.TokenData(email=email)

    except (JWTError, ValidationError):
        raise credentials_exception

    user = await user_crud.get_user_by_email(db, email=token_data.email)

    if user is None:
        raise credentials_exception

    return user
