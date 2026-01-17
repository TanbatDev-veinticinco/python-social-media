from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str

class UserCreate(User):
    password: str
    
class Post(BaseModel):
    id: int
    username: str
    title: str
    content: str
    image: Optional[str] = None
    likes: int = 0
