from dishka import Provider

from src.config.ioc.providers import (
    CacheProvider,
    DatabaseProvider,
    HttpClientProvider,
    ImageUploadServiceProvider,
    MapperProvider,
    PasswordHasherProvider,
    RedisProvider,
    RepositoryProvider,
    SessionTokenRepositoryProvider,
    SettingsProvider,
    TokenServiceProvider,
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
        RedisProvider(),
        CacheProvider(),
        SessionTokenRepositoryProvider(),
        PasswordHasherProvider(),
        TokenServiceProvider(),
        ImageUploadServiceProvider(),
        UseCaseProvider(),
        HttpClientProvider(),
    ]
