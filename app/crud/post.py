from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas import post_schema
from models.models import Post


async def get_posts(db: AsyncSession, skip : int = 0, limit: int | None = None) -> list[Post]:
    """
    Get all Posts with pagination
    """
    
    query = select(Post).order_by(Post.id.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    
    return result.scalars().all()
    

async def get_post(id: int, db: AsyncSession) -> Post | None:
    """
    Get post by ID
    """
    return await db.get_post(Post, id)
    
