from logging import config as logging_config
from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, Field, RedisDsn

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Settings class to read environment variables."""

    project_name: str
    elasticsearch_dsn: AnyHttpUrl
    redis_dsn: RedisDsn = Field(env='REDIS_FASTAPI_DSN')

    class Config:
        env_file = BASE_DIR / '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
