from fastapi import APIRouter, status, HTTPException
from schema.schema import UserCreate, UserOut
from datetime import datetime, timezone
from core.db import users_db



user_router = APIRouter()


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    #extra  validation
    for id, details in users_db.items():
       if details.username == user.username:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist!")
    if not "@" in user.email or not ".com" in user.email:
        raise ValueError("Email not valid!")
    if not len(user.password) >= 8:
        raise ValueError("Password must be up to 8 characters")
    
    user_id=str(len(users_db) + 1)
    new_user = UserOut(
        id=user_id,
        email=user.email,
        username=user.username,
        created_at=datetime.now(timezone.utc)
    )
    users_db[user_id] = new_user

    return {"message":"User successfully registered",
            "details": {"username": new_user.username, "email": new_user.email}}