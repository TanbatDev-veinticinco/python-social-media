# routes/users.py
from fastapi import APIRouter, HTTPException
from models import User, UserCreate
from storage.data import users, posts


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def register_user (user: UserCreate):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    users[user.username] = user.email
    return{"message": "User registered successfully"}

@router.get("/{username}/posts")
def get_user_posts(username: str):
    user_posts = [post for post in posts if post["username"] == username]

    if not user_posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")

    return user_posts
from fastapi import APIRouter

router = APIRouter()