from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Existing settings
    SECRET_KEY: str
    # Add these new database settings
    DB_USER: str
    DB_PASSWORD: str
    DATABASE_URL: str
    DB_NAME: str
    db_host: str = "localhost"  # optional with default value
    db_port: int = 3306  # optional with default value

    # JWT and other settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()