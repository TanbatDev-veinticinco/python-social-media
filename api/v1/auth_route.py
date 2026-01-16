from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from schemas.auth_schema import UserCreate, UserOut, UserInDB, UserUpdate
from services.auth_service import UserService
from core.db import users_db
from datetime import datetime, timezone
import uuid



auth_router = APIRouter()

#POST: create a user
@auth_router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    new_user = UserService.create_user(user_in)
    return new_user

#GET: get all user
@auth_router.get("/users", response_model=List[UserOut])
def get_all_users():
    all_users = UserService.get_all_users()
    return all_users

#POST /posts/{post_id}/like
@auth_router.post("/posts/{post_id}/like")
def like_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            post["likes"] += 1
            return {"message": "Post liked", "likes": post["likes"]}

    raise HTTPException(status_code=404, detail="Post not found")

#GET: a user by either their unique username or email
@auth_router.get("/user", response_model=UserOut)
def get_user(username: Optional[str] = None, email: Optional[str] = None):
    a_user = UserService.get_a_user_by_identifier(username=username, email=email)
    return a_user

#GET: a user by their ID
@auth_router.get("/users/user_id", response_model=UserOut)
def get_user_by_id(user_id: str):
    user = UserService.get_user_by_id(user_id)
    return user

#PATCH: partially update a user
@auth_router.patch("/users/{user_id}", response_model=UserOut)
def update_user(user_id: str, user_update: UserUpdate):
    updates = user_update.model_dump(exclude_unset=True)
    updated_user = UserService.update_user_partial(user_id, updates)
    return updated_user

#DELETE: Delete a user
@auth_router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: str):
    UserService.delete_user(user_id)
    return {"message": "user deleted successfully"}


