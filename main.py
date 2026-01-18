from fastapi import FastAPI
from routes.users import user_router
from routes.post import post_router

app = FastAPI(title="Mini social media feed")

app.include_router(user_router)
app.include_router(post_router)
