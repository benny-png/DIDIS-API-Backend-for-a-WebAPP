from fastapi import FastAPI
from .routes import user_routes

app = FastAPI()

app.include_router(user_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the User Verification API"}