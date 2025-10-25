from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from collections.abc import AsyncGenerator
from app.core.config import settings

# Creating async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionFactory = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)


# Declarative base for all models 
class Base(DeclarativeBase):
    pass
    

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session for each request.
    Ensures proper cleanup and rollback if needed.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
        
