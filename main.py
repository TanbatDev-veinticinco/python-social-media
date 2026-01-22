from fastapi import FastAPI
from routes.users import user_router
from routes.post import post_router

app = FastAPI(title="Mini social media feed")

#Versioning of API: Stood at Version 1
app.include_router(users.user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(post.post_router, prefix="/api/v1/posts", tags=["Posts"])
