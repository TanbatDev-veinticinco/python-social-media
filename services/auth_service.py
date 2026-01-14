from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from pwdlib import PasswordHash
from schemas.auth_schema import UserCreate, UserOut, UserInDB
from core.db import users_db
from datetime import datetime, timezone
import uuid



class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        password_hash = PasswordHash.recommended()
        return password_hash.hash(password)
    
    @staticmethod
    def create_user(user_in: UserCreate):
        for user in users_db.values():
            if user.username == user_in.username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")
            if user.email == user_in.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

        user_id = str(uuid.uuid4())
        new_hashed_password = UserService.hash_password(user_in.password)
        new_user = UserInDB(
            id=user_id,
            hashed_password=new_hashed_password,
            **user_in.model_dump(exclude={"password"}),
            created_at=datetime.now(timezone.utc)
        )
        users_db[user_id] = new_user
        return new_user

    @staticmethod
    def get_all_users() -> List[UserInDB]:
        users = list(users_db.values())
        if users is None:
            return {
                "message": "The user database is currently empty."
            }
        return users

    @staticmethod
    def get_a_user_by_identifier(username: Optional[str] = None, email: Optional[str] = None ):
        if not username and not email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide username or email to search")
        for user in users_db.values():
            if username and user.username == username.lower():
                return user
            if email and user.email.lower() == email.lower():
                return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username or email")
    
    @staticmethod
    def get_user_by_id(user_id: str) -> UserInDB:
        user = users_db.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this ID does not exist")
        return user

    @staticmethod
    def update_user_partial(user_id: str, updates: dict):
        user = users_db.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this ID does not exist")
        for existing in users_db.values():
            if existing.id == user_id:
                continue
            if updates.get("username") and existing.username.lower() == updates["username"].lower():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
            if updates.get("email") and existing.username.lower() == updates["email"].lower():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        if "username" in updates and updates["username"] is not None:
            user.username = updates["username"]
        if "email" in updates and updates["email"] is not None:
            user.email = updates["email"]
         # Set updated_at
        user.updated_at = datetime.now(timezone.utc)
        return user

    @staticmethod 
    def delete_user(user_id: str): 
        user = users_db.get(user_id) 
        if not user: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this ID does not exist" )
        del users_db[user_id] 
        return True
        

