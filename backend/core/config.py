# backend/core/config.py
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # ⚡ Cargamos siempre desde variables de entorno o archivo .env
    DATABASE_URL: str  # Obligatorio → definido en .env
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"  # Comma-separated URLs
    APP_NAME: str = "Marketing Dashboard"  # No sensible, puede tener default
    DEBUG: bool = True  # Para desactivar logs en producción

    def cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list."""
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]

class Config:
        env_file = ".env"   # Permite override desde .env
        case_sensitive = True


settings = Settings()
