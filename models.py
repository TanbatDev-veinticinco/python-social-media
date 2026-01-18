from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str

class Post(BaseModel):
    id: int
    username: str
    title: str
    content: str
    image: Optional[str] = None
    likes: int = 0

# Update on models.py to include UserCreate and UserOut

class UserCreate(BaseModel):
    username: str
    email: str

class UserOut(BaseModel):
    email: Optional[str] = None