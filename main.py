from fastapi import FastAPI
from routes import auth_routes
from routes import conversation_routes
from core.config import Config
import os

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.VECTOR_STORE_PATH, exist_ok=True)


app = FastAPI(
    title="Chatbot AI API",
    description="API for Chatbot AI application",
)

app.include_router(auth_routes.router, prefix="/api")
app.include_router(conversation_routes.router, prefix="/api")
