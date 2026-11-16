from typing import final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class AuthSettings(BaseSettings):
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_access_ttl: int = Field(900, alias="JWT_ACCESS_TTL")
    jwt_refresh_ttl: int = Field(2_592_000, alias="JWT_REFRESH_TTL")
    admin_email: str = Field(..., alias="ADMIN_EMAIL")
    admin_password: str = Field(..., alias="ADMIN_PASSWORD")
    admin_name: str = Field("Admin", alias="ADMIN_NAME")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
