# backend/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://app:app@db:5432/marketing"  # URL por defecto para docker
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"  # Vite dev server
    APP_NAME: str = "Marketing Dashboard"

    class Config:
        env_file = ".env"  # permite override desde .env

settings = Settings()
