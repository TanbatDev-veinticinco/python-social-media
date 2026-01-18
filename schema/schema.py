from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    role: Optional[str] = "basic_user"
    created_at: datetime

class PostOut(BaseModel):
    id: str
    title: str
    content: str
    image_path: Optional[str] = None
    image_filename: Optional[str] = None
    created_at: datetime
    user: UserOut
    likes_count: int = 0

