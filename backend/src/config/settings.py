from pydantic import Field
from pydantic_settings import BaseSettings

from src.config.app import AppSettings
from src.config.database import DatabaseSettings
from src.config.redis import RedisSettings


class Settings(BaseSettings):

	app: AppSettings = Field(default_factory=AppSettings)
	database: DatabaseSettings = Field(default_factory=DatabaseSettings)
	redis: RedisSettings = Field(default_factory=RedisSettings)


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
	def debug(self) -> bool:
		return self.app.debug
	
	@property
	def database_url(self) -> str:
		return str(self.database.sqlalchemy_data_base_url)
	
	@property
	def redis_url(self) -> str:
		return str(self.redis.redis_url)
	
	@property
	def redis_cache_ttl(self) -> int:
		return self.redis.redis_cache_ttl