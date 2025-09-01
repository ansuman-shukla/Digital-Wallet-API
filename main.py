from fastapi import FastAPI
from app_router import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Digital Wallet API"}