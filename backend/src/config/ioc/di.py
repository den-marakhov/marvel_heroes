from dishka import Provider

from src.config.ioc.providers import (
    CacheProvider,
    DatabaseProvider,
    HttpClientProvider,
    ImageUploadServiceProvider,
    MapperProvider,
    RepositoryProvider,
    SettingsProvider,
    UnitOfWorkProvider,
    UseCaseProvider,
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
        HttpClientProvider(),
    ]
