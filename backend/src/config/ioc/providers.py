from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from httpx import AsyncClient
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
import redis.asyncio as redis
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.hero.http_clients import ExternalMarvelApiProtocol
from src.application.interfaces.hero.mappers import HeroDtoEntityMapperProtocol
from src.application.interfaces.hero.repositories import HeroRepositoryProtocol
from src.application.interfaces.hero.serialization import SerializationMapperProtocol
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.user.mappers import UserDtoEntityMapperProtocol
from src.application.interfaces.user.password_hasher import PasswordHasherProtocol
from src.application.interfaces.user.repositories import UserRepositoryProtocol
from src.application.interfaces.user.serialization import (
    UserSerializationMapperProtocol,
)
from src.application.interfaces.user.session_token_repository import (
    SessionTokenRepositoryProtocol,
)
from src.application.interfaces.user.token_service import TokenServiceProtocol
from src.application.interfaces.user_session.mappers import (
    UserSessionDtoEntityMapperProtocol,
)
from src.application.interfaces.user_session.repositories import (
    UserSessionRepositoryProtocol,
)
from src.application.mappers.hero import HeroDtoEntityMapper
from src.application.mappers.user import UserDtoEntityMapper
from src.application.mappers.user_session import UserSessionDtoEntityMapper
from src.application.usecases.heroes.cache.get_hero_from_cache import (
    GetHeroFromCacheUseCase,
)
from src.application.usecases.heroes.cache.get_heroes_from_cache import (
    GetHeroesFromCacheUseCase,
)
from src.application.usecases.heroes.cache.invalidate_hero_cache import (
    InvalidateHeroCacheUseCase,
)
from src.application.usecases.heroes.cache.save_hero_to_cache import (
    SaveHeroToCacheUseCase,
)
from src.application.usecases.heroes.cache.save_heroes_to_cache import (
    SaveHeroesToCacheUseCase,
)
from src.application.usecases.heroes.external_api.enrich_hero_usecase import (
    EnrichHeroUseCase,
)
from src.application.usecases.heroes.external_api.fetch_heroes_from_external_api import (
    FetchHeroesFromExternalAPIUseCase,
)
from src.application.usecases.heroes.repo.delete_hero_from_repo import (
    DeleteHeroFromRepoUseCase,
)
from src.application.usecases.heroes.repo.get_hero_by_id_from_repo import (
    GetHeroFromRepoUseCase,
)
from src.application.usecases.heroes.repo.get_heroes_from_repo import (
    GetHeroesFromRepoUseCase,
)
from src.application.usecases.heroes.repo.save_hero_to_repo import (
    ManualHeroCreationInRepoUseCase,
)
from src.application.usecases.heroes.repo.update_hero_in_repo import (
    UpdateHeroInRepoUseCase,
)
from src.application.usecases.heroes.upload_image_usecase import UploadHeroImageUseCase
from src.application.usecases.users.auth.login import LoginUseCase
from src.application.usecases.users.auth.logout import LogoutUseCase
from src.application.usecases.users.auth.refresh import RefreshUseCase
from src.application.usecases.users.cache.get_user_by_email_from_cache import (
    GetUserByEmailFromCacheUseCase,
)
from src.application.usecases.users.cache.get_user_from_cache import (
    GetUserFromCacheUseCase,
)
from src.application.usecases.users.cache.save_user_to_cache import (
    SaveUserToCacheUseCase,
)
from src.application.usecases.users.get_current_admin import GetCurrentAdminUseCase
from src.application.usecases.users.get_current_user import GetCurrentUserUseCase
from src.application.usecases.users.repo.create_user_in_repo import (
    CreateUserInRepoUseCase,
)
from src.application.usecases.users.repo.get_user_by_email_from_repo import (
    GetUserByEmailFromRepoUseCase,
)
from src.application.usecases.users.repo.get_user_by_id_from_repo import (
    GetUserFromRepoUseCase,
)
from src.application.usecases.users.seed_admin import SeedAdminUseCase
from src.application.usecases.users.sessions.get_all_user_sessions_from_repo import (
    GetAllUserSessionsFromRepoUseCase,
)
from src.application.usecases.users.sessions.get_user_sessions_from_repo import (
    GetUserSessionsFromRepoUseCase,
)
from src.application.usecases.users.sessions.revoke_all_user_sessions_from_repo import (
    RevokeAllUserSessionsFromRepoUseCase,
)
from src.application.usecases.users.sessions.revoke_user_session_from_repo import (
    RevokeUserSessionFromRepoUseCase,
)
from src.application.usecases.users.sessions.save_user_session_to_repo import (
    SaveUserSessionToRepoUseCase,
)
from src.application.usecases.users.tokens.delete_all_user_session_tokens import (
    DeleteAllUserSessionTokensUseCase,
)
from src.application.usecases.users.tokens.delete_user_session_tokens import (
    DeleteUserSessionTokensUseCase,
)
from src.application.usecases.users.tokens.rehydrate_user_session_tokens import (
    RehydrateUserSessionTokensUseCase,
)
from src.application.usecases.users.tokens.verify_user_session_tokens import (
    VerifyUserSessionTokensUseCase,
)
from src.config.base import Settings
from src.infrastructures.cache.mappers.hero_serialization_mapper import (
    HeroSerializationMapper,
)
from src.infrastructures.cache.mappers.user_serialization_mapper import (
    UserSerializationMapper,
)
from src.infrastructures.cache.redis_client import RedisCacheClient
from src.infrastructures.db.mappers.hero_db_mapper import HeroDBMapper
from src.infrastructures.db.mappers.user_db_mapper import UserDBMapper
from src.infrastructures.db.mappers.user_session_db_mapper import UserSessionDBMapper
from src.infrastructures.db.repositories.hero import HeroRepositorySQLAlchemy
from src.infrastructures.db.repositories.user import UserRepositorySQLAlchemy
from src.infrastructures.db.repositories.user_session import (
    UserSessionRepositorySQLAlchemy,
)
from src.infrastructures.db.session import create_engine, get_session_factory
from src.infrastructures.db.uow import UnitOfWorkSQLAlchemy
from src.infrastructures.http.clients import ExternalMarvelHeroApiClient
from src.infrastructures.http.mappers.external_hero_mapper import ExternalHeroAPIMapper
from src.infrastructures.security.jwt_token_service import JwtTokenService
from src.infrastructures.security.mappers.jwt_token_mapper import JwtTokenMapper
from src.infrastructures.security.password_hasher import Argon2PasswordHasher
from src.infrastructures.security.redis_session_token_repository import (
    RedisSessionTokenRepository,
)
from src.presentation.api.rest.v1.mappers.hero_mapper import HeroPresentationMapper
from src.presentation.api.rest.v1.mappers.user_mapper import UserPresentationMapper
from src.services.image_service import ImageUploadService
from src.services.interfaces import ImageUploadServiceProtocol


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_session_factory(
        self, settings: Settings
    ) -> AsyncIterator[async_sessionmaker[AsyncSession]]:

        engine = create_engine(settings.database_url, is_echo=settings.debug)
        session_factory = get_session_factory(engine)

        try:
            yield session_factory
        finally:
            await engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:

        async with factory() as session:
            yield session


class HttpClientProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_http_client(self, settings: Settings) -> AsyncIterator[AsyncClient]:
        client = AsyncClient(follow_redirects=True, timeout=settings.http_timeout)

        try:
            yield client
        finally:
            await client.aclose()

    @provide(scope=Scope.REQUEST)
    def get_external_api_client(
        self,
        settings: Settings,
        client: AsyncClient,
        external_api_mapper: ExternalHeroAPIMapper,
    ) -> ExternalMarvelApiProtocol:
        return ExternalMarvelHeroApiClient(
            base_url=settings.external_api_base_url,
            api_key=settings.external_api_key,
            client=client,
            mapper=external_api_mapper,
        )


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_hero_repository(
        self, session: AsyncSession, db_mapper: HeroDBMapper
    ) -> HeroRepositoryProtocol:
        return HeroRepositorySQLAlchemy(session=session, mapper=db_mapper)

    @provide(scope=Scope.REQUEST)
    def get_user_repository(
        self, session: AsyncSession, user_db_mapper: UserDBMapper
    ) -> UserRepositoryProtocol:
        return UserRepositorySQLAlchemy(session=session, mapper=user_db_mapper)

    @provide(scope=Scope.REQUEST)
    def get_user_session_repository(
        self, session: AsyncSession, user_session_db_mapper: UserSessionDBMapper
    ) -> UserSessionRepositoryProtocol:
        return UserSessionRepositorySQLAlchemy(
            session=session, mapper=user_session_db_mapper
        )


class UnitOfWorkProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_unit_of_work(
        self,
        session: AsyncSession,
        hero_repository: HeroRepositoryProtocol,
        user_repository: UserRepositoryProtocol,
        user_session_repository: UserSessionRepositoryProtocol,
    ) -> UnitOfWorkProtocol:
        return UnitOfWorkSQLAlchemy(
            session=session,
            heroes=hero_repository,
            users=user_repository,
            user_sessions=user_session_repository,
        )


class MapperProvider(Provider):
    @provide(scope=Scope.APP)
    def get_hero_dto_entity_mapper(self) -> HeroDtoEntityMapperProtocol:
        return HeroDtoEntityMapper()

    @provide(scope=Scope.APP)
    def get_user_dto_entity_mapper(self) -> UserDtoEntityMapperProtocol:
        return UserDtoEntityMapper()

    @provide(scope=Scope.APP)
    def get_user_session_dto_entity_mapper(
        self,
    ) -> UserSessionDtoEntityMapperProtocol:
        return UserSessionDtoEntityMapper()

    @provide(scope=Scope.REQUEST)
    def get_hero_serialization_mapper(self) -> SerializationMapperProtocol:
        return HeroSerializationMapper()

    @provide(scope=Scope.REQUEST)
    def get_user_serialization_mapper(self) -> UserSerializationMapperProtocol:
        return UserSerializationMapper()

    @provide(scope=Scope.REQUEST)
    def get_db_mapper(self) -> HeroDBMapper:
        return HeroDBMapper()

    @provide(scope=Scope.REQUEST)
    def get_user_db_mapper(self) -> UserDBMapper:
        return UserDBMapper()

    @provide(scope=Scope.REQUEST)
    def get_user_session_db_mapper(self) -> UserSessionDBMapper:
        return UserSessionDBMapper()

    @provide(scope=Scope.REQUEST)
    def get_hero_presentation_mapper(
        self,
    ) -> HeroPresentationMapper:
        return HeroPresentationMapper()

    @provide(scope=Scope.REQUEST)
    def get_user_presentation_mapper(
        self,
    ) -> UserPresentationMapper:
        return UserPresentationMapper()

    @provide(scope=Scope.REQUEST)
    def get_external_api_hero_mapper(self) -> ExternalHeroAPIMapper:
        return ExternalHeroAPIMapper()


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_redis_client(self, settings: Settings) -> AsyncIterator[Redis]:
        client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            health_check_interval=10,
            max_connections=10,
            retry_on_timeout=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )

        try:
            yield client
        finally:
            await client.close()


class CacheProvider(Provider):
    @provide(scope=Scope.APP)
    def get_cache_client(
        self, client: Redis, settings: Settings
    ) -> CacheProtocol:
        return RedisCacheClient(client=client, ttl=settings.redis_cache_ttl)


class SessionTokenRepositoryProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_token_repository(
        self, client: Redis
    ) -> SessionTokenRepositoryProtocol:
        return RedisSessionTokenRepository(client=client, mapper=JwtTokenMapper())


class PasswordHasherProvider(Provider):
    @provide(scope=Scope.APP)
    def get_password_hash(self) -> PasswordHash:
        return PasswordHash((Argon2Hasher(),))

    @provide(scope=Scope.APP)
    def get_password_hasher(
        self, password_hash: PasswordHash
    ) -> PasswordHasherProtocol:
        return Argon2PasswordHasher(hasher=password_hash)


class TokenServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_token_service(self, settings: Settings) -> TokenServiceProtocol:
        return JwtTokenService(
            secret=settings.jwt_secret,
            access_ttl=settings.jwt_access_ttl,
            refresh_ttl=settings.jwt_refresh_ttl,
            mapper=JwtTokenMapper(),
        )


class ImageUploadServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_image_service(self, settings: Settings) -> ImageUploadServiceProtocol:
        return ImageUploadService(
            upload_dir_path=settings.upload_dir,
            temp_dir_path=settings.temp_dir,
            max_file_size=settings.max_file_size,
            allowed_mimes=settings.allowed_mimes,
            max_width=settings.max_img_width,
            max_height=settings.max_img_height,
        )


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_get_hero_from_cache_usecase(
        self,
        cache_client: CacheProtocol,
        serialization_mapper: SerializationMapperProtocol,
    ) -> GetHeroFromCacheUseCase:
        return GetHeroFromCacheUseCase(
            cache_client=cache_client, serialization_mapper=serialization_mapper
        )

    @provide(scope=Scope.REQUEST)
    def get_save_hero_to_cache_usecase(
        self,
        cache_client: CacheProtocol,
        serialization_mapper: SerializationMapperProtocol,
    ) -> SaveHeroToCacheUseCase:
        return SaveHeroToCacheUseCase(
            cache_client=cache_client, serialization_mapper=serialization_mapper
        )

    @provide(scope=Scope.REQUEST)
    def get_get_heroes_from_cache_usecase(
        self,
        cache_client: CacheProtocol,
        serialization_mapper: SerializationMapperProtocol,
    ) -> GetHeroesFromCacheUseCase:
        return GetHeroesFromCacheUseCase(
            cache_client=cache_client, serialization_mapper=serialization_mapper
        )

    @provide(scope=Scope.REQUEST)
    def get_save_heroes_to_cache(
        self,
        cache_client: CacheProtocol,
        serialization_mapper: SerializationMapperProtocol,
    ) -> SaveHeroesToCacheUseCase:
        return SaveHeroesToCacheUseCase(
            cache_client=cache_client, serialization_mapper=serialization_mapper
        )

    @provide(scope=Scope.REQUEST)
    def get_invalidate_hero_cache(
        self, cache_client: CacheProtocol
    ) -> InvalidateHeroCacheUseCase:
        return InvalidateHeroCacheUseCase(cache_client=cache_client)

    @provide(scope=Scope.REQUEST)
    def get_get_user_from_cache_usecase(
        self,
        cache_client: CacheProtocol,
        user_serialization_mapper: UserSerializationMapperProtocol,
    ) -> GetUserFromCacheUseCase:
        return GetUserFromCacheUseCase(
            cache_client=cache_client,
            serialization_mapper=user_serialization_mapper,
        )

    @provide(scope=Scope.REQUEST)
    def get_get_user_by_email_from_cache_usecase(
        self,
        cache_client: CacheProtocol,
        user_serialization_mapper: UserSerializationMapperProtocol,
    ) -> GetUserByEmailFromCacheUseCase:
        return GetUserByEmailFromCacheUseCase(
            cache_client=cache_client,
            serialization_mapper=user_serialization_mapper,
        )

    @provide(scope=Scope.REQUEST)
    def get_save_user_to_cache_usecase(
        self,
        cache_client: CacheProtocol,
        user_serialization_mapper: UserSerializationMapperProtocol,
    ) -> SaveUserToCacheUseCase:
        return SaveUserToCacheUseCase(
            cache_client=cache_client,
            serialization_mapper=user_serialization_mapper,
        )

    @provide(scope=Scope.REQUEST)
    def get_get_hero_by_id_usecase(
        self,
        hero_dto_mapper: HeroDtoEntityMapperProtocol,
        uow: UnitOfWorkProtocol,
        get_hero_from_cache_usecase: GetHeroFromCacheUseCase,
        save_hero_to_cache_usecase: SaveHeroToCacheUseCase,
    ) -> GetHeroFromRepoUseCase:
        return GetHeroFromRepoUseCase(
            uow=uow,
            mapper=hero_dto_mapper,
            get_hero_from_cache_usecase=get_hero_from_cache_usecase,
            save_hero_to_cache_usecase=save_hero_to_cache_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_get_heroes_from_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        hero_dto_mapper: HeroDtoEntityMapperProtocol,
        get_heroes_from_cache_usecase: GetHeroesFromCacheUseCase,
        save_heroes_to_cache_usecase: SaveHeroesToCacheUseCase,
    ) -> GetHeroesFromRepoUseCase:
        return GetHeroesFromRepoUseCase(
            uow=uow,
            mapper=hero_dto_mapper,
            get_heroes_from_cache_usecase=get_heroes_from_cache_usecase,
            save_heroes_to_cache_usecase=save_heroes_to_cache_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_save_hero_to_repo_usecase(
        self,
        hero_dto_mapper: HeroDtoEntityMapperProtocol,
        uow: UnitOfWorkProtocol,
        invalidate_cache_usecase: InvalidateHeroCacheUseCase,
    ) -> ManualHeroCreationInRepoUseCase:
        return ManualHeroCreationInRepoUseCase(
            uow=uow,
            mapper=hero_dto_mapper,
            invalidate_cache_usecase=invalidate_cache_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_delete_hero_from_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        image_service: ImageUploadServiceProtocol,
        invalidate_hero_cache_usecase: InvalidateHeroCacheUseCase,
    ) -> DeleteHeroFromRepoUseCase:
        return DeleteHeroFromRepoUseCase(
            uow=uow, invalidate_cache_usecase=invalidate_hero_cache_usecase, image_service=image_service
        )

    @provide(scope=Scope.REQUEST)
    def get_update_hero_in_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        mapper: HeroDtoEntityMapperProtocol,
        get_get_hero_from_repo_by_id_usecase: GetHeroFromRepoUseCase,
        get_invalidate_hero_cache_usecase: InvalidateHeroCacheUseCase,
    ) -> UpdateHeroInRepoUseCase:
        return UpdateHeroInRepoUseCase(
            uow=uow,
            mapper=mapper,
            get_hero_from_repo_by_id_usecase=get_get_hero_from_repo_by_id_usecase,
            invalidate_cache_usecase=get_invalidate_hero_cache_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_fetch_heroes_from_external_api_usecase(
        self, api_client: ExternalMarvelApiProtocol
    ) -> FetchHeroesFromExternalAPIUseCase:
        return FetchHeroesFromExternalAPIUseCase(marvel_hero_api_client=api_client)

    @provide(scope=Scope.REQUEST)
    def get_enrich_hero_usecase(
        self,
        api_client: ExternalMarvelApiProtocol,
        mapper: HeroDtoEntityMapperProtocol,
        update_hero_in_repo_usecase: UpdateHeroInRepoUseCase,
    ) -> EnrichHeroUseCase:
        return EnrichHeroUseCase(
            marvel_hero_api_client=api_client,
            mapper=mapper,
            update_hero_in_repo_usecase=update_hero_in_repo_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_upload_image_usecase(
        self,
        image_service: ImageUploadServiceProtocol,
        get_hero_from_repo_usecase: GetHeroFromRepoUseCase,
        update_hero_in_repo_usecase: UpdateHeroInRepoUseCase,
    ) -> UploadHeroImageUseCase:
        return UploadHeroImageUseCase(
            image_service=image_service,
            get_hero_from_repo_usecase=get_hero_from_repo_usecase,
            update_hero_in_repo_usecase=update_hero_in_repo_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_user_from_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        user_dto_mapper: UserDtoEntityMapperProtocol,
        get_user_from_cache_usecase: GetUserFromCacheUseCase,
        save_user_to_cache_usecase: SaveUserToCacheUseCase,
    ) -> GetUserFromRepoUseCase:
        return GetUserFromRepoUseCase(
            uow=uow,
            mapper=user_dto_mapper,
            get_user_from_cache_usecase=get_user_from_cache_usecase,
            save_user_to_cache_usecase=save_user_to_cache_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_user_by_email_from_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        user_dto_mapper: UserDtoEntityMapperProtocol,
        get_user_by_email_from_cache_usecase: GetUserByEmailFromCacheUseCase,
        save_user_to_cache_usecase: SaveUserToCacheUseCase,
    ) -> GetUserByEmailFromRepoUseCase:
        return GetUserByEmailFromRepoUseCase(
            uow=uow,
            mapper=user_dto_mapper,
            get_user_by_email_from_cache_usecase=get_user_by_email_from_cache_usecase,
            save_user_to_cache_usecase=save_user_to_cache_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_create_user_in_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        user_dto_mapper: UserDtoEntityMapperProtocol,
        save_user_to_cache_usecase: SaveUserToCacheUseCase,
    ) -> CreateUserInRepoUseCase:
        return CreateUserInRepoUseCase(
            uow=uow,
            mapper=user_dto_mapper,
            save_user_to_cache_usecase=save_user_to_cache_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_login_usecase(
        self,
        get_user_by_email_from_repo_usecase: GetUserByEmailFromRepoUseCase,
        password_hasher: PasswordHasherProtocol,
        token_service: TokenServiceProtocol,
        user_session_dto_mapper: UserSessionDtoEntityMapperProtocol,
        save_user_session_to_repo_usecase: SaveUserSessionToRepoUseCase,
    ) -> LoginUseCase:
        return LoginUseCase(
            get_user_by_email_from_repo_usecase=get_user_by_email_from_repo_usecase,
            password_hasher=password_hasher,
            token_service=token_service,
            mapper=user_session_dto_mapper,
            save_user_session_to_repo_usecase=save_user_session_to_repo_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_refresh_usecase(
        self,
        get_user_from_repo_usecase: GetUserFromRepoUseCase,
        token_service: TokenServiceProtocol,
        session_token_repository: SessionTokenRepositoryProtocol,
        verify_user_session_tokens_usecase: VerifyUserSessionTokensUseCase,
        uow: UnitOfWorkProtocol,
    ) -> RefreshUseCase:
        return RefreshUseCase(
            get_user_from_repo_usecase=get_user_from_repo_usecase,
            token_service=token_service,
            session_token_repository=session_token_repository,
            verify_user_session_tokens_usecase=verify_user_session_tokens_usecase,
            uow=uow,
        )

    @provide(scope=Scope.REQUEST)
    def get_logout_usecase(
        self,
        token_service: TokenServiceProtocol,
        verify_user_session_tokens_usecase: VerifyUserSessionTokensUseCase,
        delete_user_session_tokens_usecase: DeleteUserSessionTokensUseCase,
        uow: UnitOfWorkProtocol,
    ) -> LogoutUseCase:
        return LogoutUseCase(
            token_service=token_service,
            verify_user_session_tokens_usecase=(
                verify_user_session_tokens_usecase
            ),
            delete_user_session_tokens_usecase=(
                delete_user_session_tokens_usecase
            ),
            uow=uow,
        )

    @provide(scope=Scope.REQUEST)
    def get_current_user_usecase(
        self,
        get_user_from_repo_usecase: GetUserFromRepoUseCase,
        token_service: TokenServiceProtocol,
        verify_user_session_tokens_usecase: VerifyUserSessionTokensUseCase,
    ) -> GetCurrentUserUseCase:
        return GetCurrentUserUseCase(
            get_user_from_repo_usecase=get_user_from_repo_usecase,
            token_service=token_service,
            verify_user_session_tokens_usecase=verify_user_session_tokens_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_current_admin_usecase(
        self,
        get_current_user_usecase: GetCurrentUserUseCase,
    ) -> GetCurrentAdminUseCase:
        return GetCurrentAdminUseCase(
            get_current_user_usecase=get_current_user_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_seed_admin_usecase(
        self,
        create_user_in_repo_usecase: CreateUserInRepoUseCase,
    ) -> SeedAdminUseCase:
        return SeedAdminUseCase(
            create_user_in_repo_usecase=create_user_in_repo_usecase,
        )

    @provide(scope=Scope.REQUEST)
    def get_verify_user_session_tokens_usecase(
        self,
        session_token_repository: SessionTokenRepositoryProtocol,
        rehydrate_user_session_tokens_usecase: RehydrateUserSessionTokensUseCase,
    ) -> VerifyUserSessionTokensUseCase:
        return VerifyUserSessionTokensUseCase(
            session_token_repository=session_token_repository,
            rehydrate_user_session_tokens_usecase=(
                rehydrate_user_session_tokens_usecase
            ),
        )

    @provide(scope=Scope.REQUEST)
    def get_rehydrate_user_session_tokens_usecase(
        self,
        uow: UnitOfWorkProtocol,
        session_token_repository: SessionTokenRepositoryProtocol,
        user_session_dto_mapper: UserSessionDtoEntityMapperProtocol,
    ) -> RehydrateUserSessionTokensUseCase:
        return RehydrateUserSessionTokensUseCase(
            uow=uow,
            session_token_repository=session_token_repository,
            mapper=user_session_dto_mapper,
        )

    @provide(scope=Scope.REQUEST)
    def get_delete_user_session_tokens_usecase(
        self,
        session_token_repository: SessionTokenRepositoryProtocol,
    ) -> DeleteUserSessionTokensUseCase:
        return DeleteUserSessionTokensUseCase(
            session_token_repository=session_token_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_delete_all_user_session_tokens_usecase(
        self,
        session_token_repository: SessionTokenRepositoryProtocol,
    ) -> DeleteAllUserSessionTokensUseCase:
        return DeleteAllUserSessionTokensUseCase(
            session_token_repository=session_token_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_save_user_session_to_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        session_token_repository: SessionTokenRepositoryProtocol,
        user_session_dto_mapper: UserSessionDtoEntityMapperProtocol,
    ) -> SaveUserSessionToRepoUseCase:
        return SaveUserSessionToRepoUseCase(
            uow=uow,
            session_token_repository=session_token_repository,
            mapper=user_session_dto_mapper,
        )

    @provide(scope=Scope.REQUEST)
    def get_get_user_sessions_from_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        user_session_dto_mapper: UserSessionDtoEntityMapperProtocol,
    ) -> GetUserSessionsFromRepoUseCase:
        return GetUserSessionsFromRepoUseCase(
            uow=uow,
            mapper=user_session_dto_mapper,
        )

    @provide(scope=Scope.REQUEST)
    def get_get_all_user_sessions_from_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        user_session_dto_mapper: UserSessionDtoEntityMapperProtocol,
    ) -> GetAllUserSessionsFromRepoUseCase:
        return GetAllUserSessionsFromRepoUseCase(
            uow=uow,
            mapper=user_session_dto_mapper,
        )

    @provide(scope=Scope.REQUEST)
    def get_revoke_user_session_from_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        delete_user_session_tokens_usecase: DeleteUserSessionTokensUseCase,
    ) -> RevokeUserSessionFromRepoUseCase:
        return RevokeUserSessionFromRepoUseCase(
            uow=uow,
            delete_user_session_tokens_usecase=(
                delete_user_session_tokens_usecase
            ),
        )

    @provide(scope=Scope.REQUEST)
    def get_revoke_all_user_sessions_from_repo_usecase(
        self,
        uow: UnitOfWorkProtocol,
        delete_all_user_session_tokens_usecase: DeleteAllUserSessionTokensUseCase,
    ) -> RevokeAllUserSessionsFromRepoUseCase:
        return RevokeAllUserSessionsFromRepoUseCase(
            uow=uow,
            delete_all_user_session_tokens_usecase=(
                delete_all_user_session_tokens_usecase
            ),
        )
