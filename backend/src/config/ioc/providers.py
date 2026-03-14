from collections.abc import AsyncIterator

from httpx import AsyncClient

import redis.asyncio as redis
from dishka import Provider, Scope, provide

from sqlalchemy.ext.asyncio import (
	AsyncSession,
	async_sessionmaker
	)

from src.config.base import Settings
from src.infrastructures.db.session import get_session_factory, create_engine

from src.application.interfaces.mappers import DtoEntityMapperProtocol
from src.application.mappers import HeroMapper
from src.application.interfaces.serialization import SerializationMapperProtocol
from src.application.interfaces.repositories import HeroRepositoryProtocol
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.http_clients import ExternalMarvelApiProtocol


from src.application.usecases.repo.get_hero_by_id_from_repo import GetHeroFromRepoUseCase
from src.application.usecases.repo.get_heroes_from_repo import GetHeroesFromRepoUseCase
from src.application.usecases.repo.delete_hero_from_repo import DeleteHeroFromRepoUseCase
from src.application.usecases.repo.save_hero_to_repo import ManualHeroCreationInRepoUseCase
from src.application.usecases.repo.update_hero_in_repo import UpdateHeroInRepoUseCase
from src.application.usecases.cache.get_hero_from_cache import GetHeroFromCacheUseCase
from src.application.usecases.cache.get_heroes_from_cache import GetHeroesFromCacheUseCase
from src.application.usecases.cache.invalidate_hero_cache import InvalidateHeroCacheUseCase
from src.application.usecases.cache.save_hero_to_cache import SaveHeroToCacheUseCase
from src.application.usecases.cache.save_heroes_to_cache import SaveHeroesToCacheUseCase
from src.application.usecases.external_api.enrich_hero_usecase import EnrichHeroUseCase
from src.application.usecases.external_api.fetch_heroes_from_external_api import FetchHeroesFromExternalAPIUseCase

from src.infrastructures.db.mappers.hero_db_mapper import HeroDBMapper
from src.infrastructures.mappers.hero import HeroSerializationMapper
from src.infrastructures.db.repositories.hero import HeroRepositorySQLAlchemy
from src.infrastructures.db.uow import UnitOfWorkSQLAlchemy
from src.infrastructures.cache.redis_client import RedisCacheClient
from src.infrastructures.http.mappers.external_hero_mapper import ExternalHeroAPIMapper
from src.infrastructures.http.clients import ExternalMarvelHeroApiClient

from src.presentation.api.rest.v1.mappers.hero_mapper import HeroPresentationMapper


class SettingsProvider(Provider):

	@provide(scope=Scope.APP)
	def get_settings(self) -> Settings:
		return Settings()
	
class DatabaseProvider(Provider):

	@provide(scope=Scope.APP)
	async def get_session_factory(
		self,
		settings: Settings
		) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
				
				engine = create_engine(settings.database_url, is_echo=settings.debug)
				session_factory = get_session_factory(engine)
				
				try:
					yield session_factory
				finally:
					await engine.dispose()

	@provide(scope=Scope.REQUEST)
	async def get_session(
		self,
		factory: async_sessionmaker[AsyncSession]
	) -> AsyncIterator[AsyncSession]:
		
		async with factory() as session:
			yield session

class HttpClientProvider(Provider):

	@provide(scope=Scope.APP)
	async def get_http_client(
		self,
		settings: Settings	
	) -> AsyncIterator[AsyncClient]:
		client = AsyncClient(
			follow_redirects=True,
			timeout=settings.http_timeout
		)

		try:
			yield client
		finally:
			await client.aclose()

	@provide(scope=Scope.REQUEST)
	def get_external_api_client(
		self,
		settings: Settings,
		client: AsyncClient,
		external_api_mapper: ExternalHeroAPIMapper
	) -> ExternalMarvelApiProtocol:
		return ExternalMarvelHeroApiClient(
			base_url=settings.external_api_base_url,
			api_key=settings.external_api_key,
			client=client,
			mapper=external_api_mapper
		)

class RepositoryProvider(Provider):

	@provide(scope=Scope.REQUEST)
	def get_hero_repository(
		self,
		session: AsyncSession,
		db_mapper: HeroDBMapper
		) -> HeroRepositoryProtocol:
		return HeroRepositorySQLAlchemy(
			session=session, mapper=db_mapper
		)
	
class UnitOfWorkProvider(Provider):

	@provide(scope=Scope.REQUEST)
	def get_unit_of_work(
		self,
		session: AsyncSession,
		hero_repository: HeroRepositoryProtocol
		) -> UnitOfWorkProtocol:
		return UnitOfWorkSQLAlchemy(
			session=session, repository=hero_repository
			)

class MapperProvider(Provider):

	@provide(scope=Scope.APP)
	def get_hero_dto_entity_mapper(self) -> DtoEntityMapperProtocol:
		return HeroMapper()
	
	@provide(scope=Scope.REQUEST)
	def get_hero_serialization_mapper(self) -> SerializationMapperProtocol:
		return HeroSerializationMapper()
	
	@provide(scope=Scope.REQUEST)
	def get_db_mapper(self) -> HeroDBMapper:
		return HeroDBMapper()
	
	@provide(scope=Scope.REQUEST)
	def get_presentation_mapper(self) -> HeroPresentationMapper:
		return HeroPresentationMapper()
	
	@provide(scope=Scope.REQUEST)
	def get_external_api_hero_mapper(self) -> ExternalHeroAPIMapper:
		return ExternalHeroAPIMapper()


class CacheProvider(Provider):

	@provide(scope=Scope.APP)
	async def get_cache_client(
		self, settings: Settings
	) -> AsyncIterator[CacheProtocol]:

		redis_client = redis.from_url(
			settings.redis_url,
			encoding="utf-8",
			decode_responses=True,
			health_check_interval=10,
			max_connections=10,
			retry_on_timeout=True,
      socket_connect_timeout=5,
      socket_timeout=5,
		)

		cache_service = RedisCacheClient(
			client=redis_client, ttl=settings.redis_cache_ttl
		)

		try:
				yield cache_service
		finally:
				await cache_service.close()


class UseCaseProvider(Provider):
	
	@provide(scope=Scope.REQUEST)
	def get_get_hero_from_cache_usecase(
		self,
		cache_client: CacheProtocol,
		serialization_mapper: SerializationMapperProtocol
	) -> GetHeroFromCacheUseCase:
		return GetHeroFromCacheUseCase(
			cache_client=cache_client, serialization_mapper=serialization_mapper
		)
	
	@provide(scope=Scope.REQUEST)
	def get_save_hero_to_cache_usecase(
		self,
		cache_client: CacheProtocol,
		serialization_mapper: SerializationMapperProtocol
	) -> SaveHeroToCacheUseCase:
		return SaveHeroToCacheUseCase(
			cache_client=cache_client,
			serialization_mapper=serialization_mapper
		)
	
	@provide(scope=Scope.REQUEST)
	def get_get_heroes_from_cache_usecase(
		self,
		cache_client: CacheProtocol,
		serialization_mapper: SerializationMapperProtocol
	) -> GetHeroesFromCacheUseCase:
		return GetHeroesFromCacheUseCase(
			cache_client=cache_client,
			serialization_mapper=serialization_mapper
		)
	
	@provide(scope=Scope.REQUEST)
	def get_save_heroes_to_cache(
		self,
		cache_client: CacheProtocol,
		serialization_mapper: SerializationMapperProtocol
	) -> SaveHeroesToCacheUseCase:
		return SaveHeroesToCacheUseCase(
			cache_client=cache_client,
			serialization_mapper=serialization_mapper
		)
	
	@provide(scope=Scope.REQUEST)
	def get_invalidate_hero_cache(
		self,
		cache_client: CacheProtocol
	) -> InvalidateHeroCacheUseCase:
		return InvalidateHeroCacheUseCase(cache_client=cache_client)

	@provide(scope=Scope.REQUEST)
	def get_get_hero_by_id_usecase(
		self,
		hero_dto_mapper: DtoEntityMapperProtocol,
		uow: UnitOfWorkProtocol,
		get_hero_from_cache_usecase: GetHeroFromCacheUseCase,
		save_hero_to_cache_usecase: SaveHeroToCacheUseCase,
	) -> GetHeroFromRepoUseCase:
		return GetHeroFromRepoUseCase(
			uow=uow,
			mapper=hero_dto_mapper,
			get_hero_from_cache_usecase=get_hero_from_cache_usecase,
			save_hero_to_cache_usecase=save_hero_to_cache_usecase
		)
	
	@provide(scope=Scope.REQUEST)
	def get_get_heroes_from_repo_usecase(
		self,
		uow: UnitOfWorkProtocol,
		hero_dto_mapper: DtoEntityMapperProtocol,
		get_heroes_from_cache_usecase: GetHeroesFromCacheUseCase,
		save_heroes_to_cache_usecase: SaveHeroesToCacheUseCase
	) -> GetHeroesFromRepoUseCase:
		return GetHeroesFromRepoUseCase(
			uow=uow,
			mapper=hero_dto_mapper,
			get_heroes_from_cache_usecase=get_heroes_from_cache_usecase,
			save_heroes_to_cache_usecase=save_heroes_to_cache_usecase
		)
	
	@provide(scope=Scope.REQUEST)
	def get_save_hero_to_repo_usecase(
		self,
		hero_dto_mapper: DtoEntityMapperProtocol,
		uow: UnitOfWorkProtocol,
		invalidate_cache_usecase: InvalidateHeroCacheUseCase
	) -> ManualHeroCreationInRepoUseCase:
		return ManualHeroCreationInRepoUseCase(
			uow=uow,
			mapper=hero_dto_mapper,
			invalidate_cache_usecase=invalidate_cache_usecase
		)
	
	@provide(scope=Scope.REQUEST)
	def get_delete_hero_from_repo_usecase(
		self,
		uow: UnitOfWorkProtocol,
		invalidate_hero_cache_usecase: InvalidateHeroCacheUseCase
		) -> DeleteHeroFromRepoUseCase:
		return DeleteHeroFromRepoUseCase(
			uow=uow,
			invalidate_cache_usecase=invalidate_hero_cache_usecase
		)
	
	@provide(scope=Scope.REQUEST)
	def get_update_hero_in_repo_usecase(
		self,
		uow: UnitOfWorkProtocol,
		mapper: DtoEntityMapperProtocol,
		get_get_hero_from_repo_by_id_usecase: GetHeroFromRepoUseCase,
		get_invalidate_hero_cache_usecase: InvalidateHeroCacheUseCase
	) -> UpdateHeroInRepoUseCase:
		return UpdateHeroInRepoUseCase(
			uow=uow,
			mapper=mapper,
			get_hero_from_repo_by_id_usecase=get_get_hero_from_repo_by_id_usecase,
			invalidate_cache_usecase=get_invalidate_hero_cache_usecase
		)
	
	@provide(scope=Scope.REQUEST)
	def get_fetch_heroes_from_external_api_usecase(
		self,
		api_client: ExternalMarvelApiProtocol
	) -> FetchHeroesFromExternalAPIUseCase:
		return FetchHeroesFromExternalAPIUseCase(
			marvel_hero_api_client=api_client
		)
	
	@provide(scope=Scope.REQUEST)
	def get_enrich_hero_usecase(
		self,
		api_client: ExternalMarvelApiProtocol,
		mapper: DtoEntityMapperProtocol,
		update_hero_in_repo_usecase: UpdateHeroInRepoUseCase
	) -> EnrichHeroUseCase:
		return EnrichHeroUseCase(
			marvel_hero_api_client=api_client,
			mapper=mapper,
			update_hero_in_repo_usecase=update_hero_in_repo_usecase
		)
