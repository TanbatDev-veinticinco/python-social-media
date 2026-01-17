from fastapi import APIRouter, HTTPException, status, Form, File, UploadFile
from typing import Optional
from core.db import UPLOAD_DIR, posts_db, users_db
from schema.schema import PostOut
from datetime import datetime, timezone
import os


post_router = APIRouter()


#function that saves the image
# def save_image(image: Optional[UploadFile]) -> Optional[str]:
#     if not image:
#         return None
    
#     filename = f"{len(posts_db)+1}_{image.filename}"
#     filepath = os.path.join(UPLOAD_DIR, filename)

#     with open(filepath, "wb") as buffer:
#         buffer.write(image.file.read())
#         return filename

@post_router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    username: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    author = None
    for u in users_db.values():
        if u.username == username:
            author = u
            break
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="username not found. You must be registered to post.")
    post_id = str(len(posts_db) + 1)

    #handling of image
    image_filename = None
    image_path = None
    if image:
        file_extension = os.path.splitext(image.filename)[1]
        filename = f"{post_id}{file_extension}"
        image_path = os.path.join(UPLOAD_DIR, filename)

        content_bytes = await image.read()
        print("Bytes received:", len(content_bytes))
        with open(image_path, "wb") as buffer:
            buffer.write(content_bytes)

        image_filename = filename
        
    #create new post
    new_post = PostOut(
        id=post_id,
        title=title,
        content=content,
        image_path=image_path,
        image_filename=image_filename,
        created_at=datetime.now(timezone.utc),
        user=author,
        likes_count=0
    )
    posts_db[post_id] = new_post
    return new_post


     



