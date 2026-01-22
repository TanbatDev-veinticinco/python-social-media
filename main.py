from fastapi import FastAPI
from routes import users, post

app = FastAPI(title="Mini social media feed")

@app.get("/")
def home():
    return {"message": "Welcome to Mini Social Media Feed API"}

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])

