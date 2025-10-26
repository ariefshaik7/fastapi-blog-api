from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    password: str 
    
class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    model_config: ConfigDict = ConfigDict(from_attributes=True)
    
    
    
    