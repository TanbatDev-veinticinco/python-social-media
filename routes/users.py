from fastapi import APIRouter, status
from models import UserCreate
router = APIRouter()

users_db = {}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    #extra  validation
    for id, details in users_db.items():
       if details.username == user.username:
           raise ValueError("Username already exist!")
    if not "@" in user.email or not ".com" in user.email:
        raise ValueError("Email not valid!")
    if not len(user.password) >= 8:
        raise ValueError("Password must be up to 8 characters")
    
    user_id=len(users_db) + 1
    db_user = user.model_dump()
    db_user["id"] = user_id
    users_db[user_id] =db_user

    return {"message":"User successfully registered",
            "details": {"username": db_user["username"], "email": db_user["email"]}}