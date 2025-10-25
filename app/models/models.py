from typing import override
from sqlalchemy import Integer, String, Text, DateTime, func
from app.db.session import Base
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime


class Post(Base):
    """
    Model for Blog Post
    """
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now())
    
    # Dunder Method / Magic Method
    @override
    def __repr__(self) -> str:
        return f"<Post(id={self.id!r}, title={self.title!r})>"
    