from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime


#this will be the base schema
class UserBase(BaseModel):
    username: str
    email: EmailStr
#this schema creates new user 
class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    role: Optional[str] = "basic_user"
    created_at: datetime
    
class UserInDB(UserOut):
    hashed_password: str
    updated_at: Optional[datetime] = None

class UserUpdate(BaseModel): 
    username: Optional[str] = None 
    email: Optional[EmailStr] = None

