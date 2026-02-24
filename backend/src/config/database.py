from typing import final

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

@final
class DatabaseSettings(BaseSettings):

	postgres_user: str = Field(..., alias="POSTGRES_USER")
	postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
	postgres_host: str = Field(..., alias="POSTGRES_HOST")
	postgres_port: int = Field(..., alias="POSTGRES_PORT")
	postgres_db: str = Field(..., alias="POSTGRES_DB_NAME")

	@property
	def sqlalchemy_data_base_url(self) -> PostgresDsn:
		return PostgresDsn.build(
			scheme="postgresql+asyncpg",
			username=self.postgres_user,
			password=self.postgres_password,
			host=self.postgres_host,
			port=self.postgres_port,
			path=self.postgres_db
		)



	model_config=SettingsConfigDict(
		env_file='.env',
		env_file_encoding='utf-8',
		extra='ignore'
	)