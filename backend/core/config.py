# backend/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ⚡ Cargamos siempre desde variables de entorno o archivo .env
    DATABASE_URL: str  # Obligatorio → definido en .env
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"  # Default seguro
    APP_NAME: str = "Marketing Dashboard"  # No sensible, puede tener default
    DEBUG: bool = True  # Para desactivar logs en producción

    class Config:
        env_file = ".env"   # Permite override desde .env
        case_sensitive = True


settings = Settings()
