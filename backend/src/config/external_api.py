from typing import final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class ExternalAPISettings(BaseSettings):

	heroes_api_base: str = Field(
		"https://superheroapi.com/api", alias="MARVEL_HEROES_API_BASE"
	)
	api_key: str = Field(
		..., alias="MARVEL_API_KEY"
	)
	http_timeout: float = Field(10.0, alias="HTTP_TIMEOUT")

	model_config=SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra='ignore'
	)