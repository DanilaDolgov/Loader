import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    rabbit_dsn: str = os.getenv('RABBITMQ_DSN', '')
    DSN_MINIO: str = os.getenv('DSN_MINIO', '')
    MINIO_ACCESS_KEY: str = os.getenv('MINIO_ACCESS_KEY', '')
    MINIO_SECRET_KEY: str = os.getenv('MINIO_SECRET_KEY', '')
    MINIO_BUCKET_NAME: str = os.getenv('MINIO_BUCKET_NAME', '')
    DSN_REDIS: str = os.getenv('DSN_REDIS')

    # PostgreSQL
    DB_PORT: int = Field(default=..., ge=1)
    DB_HOST: str = Field(default=..., min_length=1)
    DB_USER: str = Field(default=..., min_length=1)
    DB_PASS: str = Field(default=..., min_length=1)
    DB_NAME: str = Field(default=..., min_length=1)
    DB_SCHEMA: str = Field(default=..., min_length=1)

    REDIS_COOKIE_NAME: str = Field(default=..., min_length=1)
    BASE_URL: str =  Field(default=..., min_length=1)

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
