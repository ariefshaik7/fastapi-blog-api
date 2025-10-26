from typing import override
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, DateTime, func
from app.db.session import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime


class User(Base):
    """
    Model for User
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    posts: Mapped[list["Post"]] = relationship(
        "Posts", back_populates="owner", cascade="all, delete-orphan"
    )

    # Dunder Method / Magic Method
    @override
    def __repr__(self) -> str:
        return f"<User(email='{self.email}')>"


class Post(Base):
    """
    Model for Post
    """

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner: Mapped["User"] = relationship("User", back_populates="posts")

    # Dunder Method / Magic Method
    @override
    def __repr__(self) -> str:
        return f"<Post(id={self.id!r}, title={self.title!r})>"
