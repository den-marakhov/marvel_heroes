from dishka import Provider

from src.config.ioc.providers import (
	SettingsProvider,
	DatabaseProvider,
	RepositoryProvider,
	UnitOfWorkProvider,
	MapperProvider,
	CacheProvider,
	ImageUploadServiceProvider,
	UseCaseProvider,
	HttpClientProvider
)

def get_providers() -> list[Provider]:
	return [
		SettingsProvider(),
		DatabaseProvider(),
		RepositoryProvider(),
		UnitOfWorkProvider(),
		MapperProvider(),
		CacheProvider(),
		ImageUploadServiceProvider(),
		UseCaseProvider(),
		HttpClientProvider()
	]