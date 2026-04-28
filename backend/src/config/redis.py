from typing import final

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class RedisSettings(BaseSettings):
    redis_password: str = Field("redis_password", alias="REDIS_PASSWORD")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    redis_host: str = Field("redis_host", alias="REDIS_HOST")
    redis_db: int = Field(0, alias="REDIS_DB")
    redis_cache_ttl: int = Field(360, alias="REDIS_TTL")

    @property
    def redis_url(self) -> RedisDsn:

        return RedisDsn.build(
            scheme="redis",
            password=self.redis_password,
            host=self.redis_host,
            port=self.redis_port,
            path=str(self.redis_db),
        )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
