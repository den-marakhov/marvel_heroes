from pydantic import Field
from pydantic_settings import BaseSettings

from src.config.app import AppSettings
from src.config.database import DatabaseSettings
from src.config.redis import RedisSettings
from src.config.external_api import ExternalAPISettings
from src.config.image_service_settings import ImageServiceSettings


class Settings(BaseSettings):

	app: AppSettings = Field(default_factory=AppSettings)
	database: DatabaseSettings = Field(default_factory=DatabaseSettings)
	redis: RedisSettings = Field(default_factory=RedisSettings)
	external_api: ExternalAPISettings = Field(default_factory=ExternalAPISettings)
	image_service_settings: ImageServiceSettings = Field(
		default_factory=ImageServiceSettings
	)


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
	def base_url(self) -> str:
		return self.app.base_url
	
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
	
	@property
	def external_api_base_url(self) -> str:
		return self.external_api.heroes_api_base
	
	@property
	def external_api_key(self) -> str:
		return self.external_api.api_key
	
	@property
	def http_timeout(self) -> float:
		return self.external_api.http_timeout
	
	@property
	def max_img_width(self) -> int:
		return self.image_service_settings.img_width
	
	@property
	def max_img_height(self) -> int:
		return self.image_service_settings.img_height
	
	@property
	def max_file_size(self) -> int:
		return self.image_service_settings.max_file_size
	
	@property
	def temp_dir(self) -> str:
		return self.image_service_settings.temp_dir
	
	@property
	def upload_dir(self) -> str:
		return self.image_service_settings.upload_dir
	
	@property
	def allowed_mimes(self) -> list[str]:
		return self.image_service_settings.allowed_types