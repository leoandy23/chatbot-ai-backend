from fastapi import FastAPI
from routes.auth_routes import router as auth_router


app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")


@app.get("/")
async def root():
    return {"Hello": "World"}
