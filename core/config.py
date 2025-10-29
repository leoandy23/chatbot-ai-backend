from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    ALGORITHM = "HS256"
    UPLOAD_FOLDER = "uploads"
    VECTOR_STORE_PATH = "vector_db"
    EMBEDDING_MODEL = "text-embedding-3-small"
