# routes/users.py
from fastapi import APIRouter, status, HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from schemas.schema import UserCreate, UserOut, PostOut, UserUpdate
from datetime import datetime, timezone
from core.db import users_db, posts_db
from typing import List


user_router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

#A dependency to get current user
#This dependency will work with the /posts/{post_id}/like endpoint
def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    user = None
    for u in users_db.values():
        if u.username == token:
            user = u
            break
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

    
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

#List all posts by a user
@user_router.get("/{username}/posts", response_model=List[PostOut])
def get_users_posts(username: str)-> List[dict]:
    provided_username = username.lower()
    #To check if a user exists
    user = next(
        (u for u in users_db.values() if u.username.lower() == provided_username),
        None
    )
    if user is None: 
        raise HTTPException( status_code=404, detail=f"User '{username}' does not exist" )
    user_posts = [
        post for post in posts_db.values()
        if post.user.username ==provided_username
    ]
    if not user_posts: 
        raise HTTPException(status_code=404, detail=f"User '{username}' has no posts" )
    return user_posts


@user_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in users_db.values() if u.username == form_data.username.lower()), None)
    if not user:
        return None
    return user

# Added endpoints for user details
@user_router.get("/{username}")
def get_user(username: str):
    if username not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {
        "username": username,
        "email": users[username]
    }

@user_router.put("/{username}")
def update_user(username: str, user: UserUpdate):
    db_user = next(
        (u for u in users_db.values() if u.username == username),
        None
    )
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.email:
        db_user.email = user.email
    if user.username:
        db_user.username = user.username

    return {"message": "User updated successfully"}


@user_router.delete("/{username}")
def delete_user(username: str):
    if username not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    #Remove user
    del users[username]

    #Remove user's posts
    global posts
    posts[:] = [post for post in posts if post['username'] != username]
    return {
        "message": "User and associated posts deleted",
    }

