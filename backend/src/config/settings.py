from pydantic import Field
from pydantic_settings import BaseSettings

from src.config.app import AppSettings
from src.config.database import DatabaseSettings


class Settings(BaseSettings):

	app: AppSettings = Field(default_factory=AppSettings)
	database: DatabaseSettings = Field(default_factory=DatabaseSettings)


	@property
	def app_name(self)-> str:
		return self.app.app_name
	
	@property
	def environment(self) -> str:
		return self.app.environment
	
	@property
	def log_level(self) -> str:
		return self.app.log_level
	
	@property
	def debug(self) -> str:
		return self.app.debug
	
	@property
	def database_url(self) -> str:
		return str(self.database.sqlalchemy_data_base_url)