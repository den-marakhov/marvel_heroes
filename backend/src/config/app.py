from typing import Literal,final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

@final
class AppSettings(BaseSettings):

	app_name: str = "Marvel Heroes API"
	environment: Literal["local", "dev", "development", "prod"] = "local"
	log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
	debug: bool = Field(False, alias="DEBUG")

	model_config=SettingsConfigDict(
		env_file='.env',
		env_file_encoding='utf-8',
		extra='ignore'
	)