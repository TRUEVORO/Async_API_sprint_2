from pydantic import AnyHttpUrl, BaseSettings, Field, RedisDsn


class TestSettings(BaseSettings):
    """A class that defines the TestSettings configuration model using the Pydantic BaseSettings class."""

    elasticsearch_dsn: AnyHttpUrl = Field('http://localhost:9200')
    redis_dsn: RedisDsn | AnyHttpUrl = Field('http://localhost:6379', env='REDIS_FASTAPI_DSN')
    service_dsn: AnyHttpUrl = Field('http://localhost:8000')

    # class Config:
    #     env_file = '.env.test'
    #     env_file_encoding = 'utf-8'


test_settings = TestSettings()
