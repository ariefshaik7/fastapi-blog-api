from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User
from app.schemas import user_schema
from app.auth import security
from sqlalchemy.future import select

async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    """
    Get user by email
    """
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(user: user_schema.UserCreate, db: AsyncSession) -> User:
    """
    create a new user
    """
    hashed_pass = security.hash_password(user.password)

    user.password = hashed_pass

    new_user = User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
