from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "Meu Pedaço Favorito"
    ENV: Literal["local", "development", "staging", "production"] = "local"

    DATABASE_URL: str = "postgresql+asyncpg://mpf:mpf@db:5432/mpf"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    SQLALCHEMY_ECHO: bool = False

    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_DEFAULT_DB: int = 0
    REDIS_LOCK_TTL_SECONDS: int = 30

    WORKER_QUEUE_NAME: str = "default"
    API_PREFIX: str = "/api"


settings = Settings()
