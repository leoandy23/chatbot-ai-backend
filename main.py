from fastapi import FastAPI
from routes import auth_routes
from routes import dashboard_routes


app = FastAPI(
    title="Chatbot AI API",
    description="API for Chatbot AI application",
)

app.include_router(auth_routes.router, prefix="/api")
app.include_router(dashboard_routes.router, prefix="/api")
