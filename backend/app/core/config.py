import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str = "supersecret"
    TENANT_ROUTING_MODE: str = "path"

    class Config:
        env_file = ".env"

settings = Settings()
