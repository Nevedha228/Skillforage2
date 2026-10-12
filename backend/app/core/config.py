import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "SkillForage AI")
    APP_ENV: str = os.getenv("APP_ENV", "development").lower()
    APP_URL: str = os.getenv("APP_URL", "http://localhost:5173")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-insecure-secret-key-32-chars-minimum-needed")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./skillforage.db")
    SESSION_EXPIRE_DAYS: int = int(os.getenv("SESSION_EXPIRE_DAYS", "7"))
    
    # CORS
    CORS_ORIGINS_RAW: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    
    # Email / SMTP
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "no-reply@skillforage.ai")

    # External APIs
    ADZUNA_APP_ID: str = os.getenv("ADZUNA_APP_ID", "")
    ADZUNA_APP_KEY: str = os.getenv("ADZUNA_APP_KEY", "")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")

    @property
    def is_production(self) -> bool:
        return self.APP_ENV in ("production", "prod")

    @property
    def is_development(self) -> bool:
        return self.APP_ENV in ("development", "dev")

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS_RAW.split(",") if o.strip()]

settings = Settings()
