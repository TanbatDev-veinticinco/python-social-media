from fastapi import FastAPI
from routes import users, post

app = FastAPI(title="Mini social media feed")

app.include_router(users.user_router, prefix="api/v1/users", tags=["Users"])
app.include_router(post.post_router, prefix="api/v1/posts", tags=["Posts"])
