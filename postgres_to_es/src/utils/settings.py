from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, Field, PostgresDsn, RedisDsn

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Settings model with DSN."""

    postgres_dsn: PostgresDsn
    elasticsearch_dsn: AnyHttpUrl
    redis_dsn: RedisDsn = Field(env='REDIS_ETL_DSN')
    batch_size: int
    timeout: float

    class Config:
        env_file = BASE_DIR / '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
