import pytest
from unittest.mock import AsyncMock, MagicMock

from src.application.usecases.repo.get_heroes_from_repo import GetHeroesFromRepoUseCase

from tests.factories import HeroDTOFactory, HeroEntityFactory

class TestGetHeroesFromRepoUseCase:

	@pytest.fixture
	def mock_get_heroes_from_cache_usecase(self) -> AsyncMock:
		return AsyncMock()
	
	@pytest.fixture
	def mock_save_heroes_to_cache_usecase(self) -> AsyncMock:
		return AsyncMock()
	
	
	@pytest.fixture
	def get_heroes_from_repo(
		self,
		mock_uow: AsyncMock,
		mock_mapper: MagicMock,
		mock_get_heroes_from_cache_usecase: AsyncMock,
		mock_save_heroes_to_cache_usecase: AsyncMock
	) -> GetHeroesFromRepoUseCase:
		return GetHeroesFromRepoUseCase(
			uow=mock_uow,
			mapper=mock_mapper,
			get_heroes_from_cache_usecase=mock_get_heroes_from_cache_usecase,
			save_heroes_to_cache_usecase=mock_save_heroes_to_cache_usecase
		)
	
	@pytest.mark.asyncio
	async def test_retrieve_heroes_from_cache(
			self,
			mock_uow: AsyncMock,
			get_heroes_from_repo: GetHeroesFromRepoUseCase,
			mock_get_heroes_from_cache_usecase: AsyncMock,
			mock_save_heroes_to_cache_usecase: AsyncMock
	):
		cached_heroes = HeroDTOFactory.batch(3)
		mock_get_heroes_from_cache_usecase.return_value = cached_heroes

		result = await get_heroes_from_repo()

		assert result == cached_heroes
		mock_uow.repository.get_heroes.assert_not_called()
		mock_save_heroes_to_cache_usecase.assert_not_called()

	@pytest.mark.asyncio
	async def test_retrieve_heroes_from_repo(
		self,
		mock_uow: AsyncMock,
		mock_mapper: MagicMock,
		get_heroes_from_repo: GetHeroesFromRepoUseCase,
		mock_get_heroes_from_cache_usecase: AsyncMock,
		mock_save_heroes_to_cache_usecase: AsyncMock
	):
		mock_get_heroes_from_cache_usecase.return_value = None

		heroes_entities = HeroEntityFactory.batch(3)
		mock_uow.repository.get_heroes.return_value = heroes_entities

		hero_dtos = HeroDTOFactory.batch(3)
		mock_mapper.to_dto.side_effect = hero_dtos

		result = await get_heroes_from_repo()

		assert result == hero_dtos
		mock_get_heroes_from_cache_usecase.assert_called_once()
		mock_uow.repository.get_heroes.assert_called_once()
		mock_save_heroes_to_cache_usecase.assert_called_once()




		


