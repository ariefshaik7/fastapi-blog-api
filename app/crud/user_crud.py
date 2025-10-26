from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import User
from app.schemas import user_schema
from app.auth.security import hash_password


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    """
    Get user by email
    """
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(user: user_schema.UserCreate, db: AsyncSession) -> User:
    """
    Create a new user
    """
    hashed_pass = hash_password(user.password)

    new_user_data = user.model_dump()
    new_user_data["password"] = hashed_pass

    new_user = User(**new_user_data)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
