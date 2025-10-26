from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas import user_schema
from app.crud import user_crud


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.User)
async def create_new_user(
    user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    db_user = await user_crud.get_user_by_email(email=user.email, db=db)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_user = await user_crud.create_user(user=user, db=db)

    return new_user
