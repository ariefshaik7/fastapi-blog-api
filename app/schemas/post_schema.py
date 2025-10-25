from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    """
    Base Schema for post
    """

    title: str
    content: str


class PostCreate(PostBase):
    """
    Schema to create Post
    """

    pass


class PostUpdate(BaseModel):
    """
    Schema to update Post
    """

    title: str | None = None
    content: str | None = None


class Post(PostBase):
    """
    Schema for reading/returning a post.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
