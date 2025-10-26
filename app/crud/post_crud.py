from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Post
from app.schemas import post_schema


async def get_posts(
    db: AsyncSession, skip: int = 0, limit: int | None = None
) -> list[Post]:
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
    return await db.get(Post, id)


async def create_post(
    post: post_schema.PostCreate, db: AsyncSession, owner_id: int
) -> Post:
    """
    Creating a new Post
    """
    new_post = Post(title=post.title, content=post.content, owner_id=owner_id)

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


async def update_post(
    id: int, post: post_schema.PostUpdate, db: AsyncSession
) -> Post | None:
    """
    Update a post
    """
    db_post = await get_post(id=id, db=db)

    if not db_post:
        return None

    update_post = post.model_dump(exclude_unset=True)

    for key, value in update_post.items():
        setattr(db_post, key, value)

    await db.commit()
    await db.refresh(db_post)
    # ----- Another way to do -----
    # query = select(models.Post).filter(models.Post.id == post_id)
    # result = await db.execute(query)
    # db_post = result.scalars().first()
    return db_post


async def delete_post(id: int, db: AsyncSession) -> Post | None:
    """
    Delete a post
    """
    db_post = await get_post(id=id, db=db)

    if not db_post:
        return None

    await db.delete(db_post)
    await db.commit()
    return db_post
