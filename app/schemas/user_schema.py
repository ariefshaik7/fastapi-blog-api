from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)
    
class User(BaseModel):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config: ConfigDict = ConfigDict(from_attributes=True)
    
    
    
    