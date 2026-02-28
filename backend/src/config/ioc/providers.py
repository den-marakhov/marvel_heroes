from collections.abc import AsyncIterator

from uuid import UUID

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

from src.application.usecases.get_hero_by_id_from_repo import GetHeroFromRepoUseCase
from src.application.usecases.get_heroes_from_repo import GetHeroesFromRepoUseCase
from src.application.usecases.delete_hero_from_repo import DeleteHeroFromRepoUseCase
from src.application.usecases.save_hero_to_repo import ManualHeroCreationInRepoUseCase
from src.application.usecases.get_hero_from_cache import GetHeroFromCacheUseCase
from src.application.usecases.get_heroes_from_cache import GetHeroesFromCacheUseCase
from src.application.usecases.invalidate_hero_cache import InvalidateHeroCacheUseCase
from src.application.usecases.save_hero_to_cache import SaveHeroToCacheUseCase
from src.application.usecases.save_heroes_to_cache import SaveHeroesToCacheUseCase

from src.infrastructures.db.mappers.hero_db_mapper import HeroDBMapper
from src.infrastructures.mappers.hero import HeroSerializationMapper
from src.infrastructures.db.repositories.hero import HeroRepositorySQLAlchemy
from src.infrastructures.db.uow import UnitOfWorkSQLAlchemy
from src.infrastructures.cache.redis_client import RedisCacheClient

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
