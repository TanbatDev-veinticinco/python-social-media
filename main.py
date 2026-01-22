from fastapi import FastAPI
from routes.users import user_router
from routes.post import post_router

app = FastAPI(title="Mini social media feed")

@app.get("/")
def home():
    return {"message": "Welcome to Mini Social Media Feed API"}

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(post_router, prefix="/posts", tags=["Posts"])

#Versioning of API: Stood at Version 1
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(post_router, prefix="/api/v1/posts", tags=["Posts"])
