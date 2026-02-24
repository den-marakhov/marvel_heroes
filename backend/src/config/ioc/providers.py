from collections.abc import AsyncIterator

from uuid import UUID

from dishka import Provider, Scope, provide

from sqlalchemy.ext.asyncio import (
	AsyncSession,
	async_sessionmaker
	)

from src.config.base import Settings
from src.infrastructures.db.session import get_session_factory, create_engine

from src.application.interfaces.mappers import DtoEntityMapperProtocol
from src.application.mappers import HeroMapper
from src.application.interfaces.repositories import HeroRepositoryProtocol
from src.application.interfaces.uow import UnitOfWorkProtocol

from src.application.usecases.get_hero_by_id import GetHeroFromRepoUseCase
from src.application.usecases.delete_hero_from_repo import DeleteHeroFromRepoUseCase
from src.application.usecases.save_hero_to_repo import ManualHeroCreationInRepoUseCase

from src.infrastructures.db.mappers.hero_db_mapper import HeroDBMapper
from src.infrastructures.db.repositories.hero import HeroRepositorySQLAlchemy
from src.infrastructures.db.uow import UnitOfWorkSQLAlchemy

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
	def get_hero_dto_entity_provider(self) -> DtoEntityMapperProtocol:
		return HeroMapper()
	
	@provide(scope=Scope.REQUEST)
	def get_db_mapper(self) -> HeroDBMapper:
		return HeroDBMapper()
	
	@provide(scope=Scope.REQUEST)
	def get_presentation_mapper(self) -> HeroPresentationMapper:
		return HeroPresentationMapper()
	

class UseCaseProvider(Provider):

	@provide(scope=Scope.REQUEST)
	def get_get_hero_by_id_usecase(
		self, hero_dto_mapper: DtoEntityMapperProtocol, uow: UnitOfWorkProtocol
	) -> GetHeroFromRepoUseCase:
		return GetHeroFromRepoUseCase(uow=uow, mapper=hero_dto_mapper)
	
	@provide(scope=Scope.REQUEST)
	def get_save_hero_to_repo_usecase(
		self, hero_dto_mapper: DtoEntityMapperProtocol, uow: UnitOfWorkProtocol
	) -> ManualHeroCreationInRepoUseCase:
		return ManualHeroCreationInRepoUseCase(
			uow=uow, mapper=hero_dto_mapper
		)
	
	@provide(scope=Scope.REQUEST)
	def get_delete_hero_from_repo_usecase(
		self, uow: UnitOfWorkProtocol
		) -> DeleteHeroFromRepoUseCase:
		return DeleteHeroFromRepoUseCase(uow=uow)



