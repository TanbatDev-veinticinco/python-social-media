from fastapi import FastAPI
from api.v1.auth_route import auth_router


app = FastAPI()

app.include_router(auth_router, prefix="/users", tags=["Authentication Route"])

@app.get("/")
def root():
    return {
        "message": "The version 1 mini social feed application"
    }