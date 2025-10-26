from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas import post_schema

from app.crud import post_crud
from app.models.models import User
from app.auth.auth import get_current_user


router = APIRouter()


@router.get("/", response_model=List[post_schema.Post])
async def get_all_posts(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10
):
    """
    Retrieve all posts with pagination
    """
    posts = await post_crud.get_posts(db=db, skip=skip, limit=limit)
    return posts


@router.get("/{id}", response_model=post_schema.Post)
async def get_single_post(id: int, db: AsyncSession = Depends(get_db)):
    """
    Get single post by ID
    """
    db_post = await post_crud.get_post(id=id, db=db)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} does not exist",
        )
    return db_post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post_schema.Post)
async def create_new_post(
    new_post: post_schema.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new Post
    """
    return await post_crud.create_post(
        post=new_post,
        db=db,
        owner_id=current_user.id,
    )


@router.put("/{id}", response_model=post_schema.Post)
async def update_existing_post(
    id: int,
    post: post_schema.PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a post by its ID
    """
    db_post = await post_crud.get_post(id=id, db=db)

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not exist",
        )

    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )

    updated_post = await post_crud.update_post(id=id, post=post, db=db)

    return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_post(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Deleting a Post by its ID
    """
    db_post = await post_crud.get_post(id=id, db=db)

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} does not exist",
        )

    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post",
        )

    await post_crud.delete_post(id=id, db=db)

    return None
