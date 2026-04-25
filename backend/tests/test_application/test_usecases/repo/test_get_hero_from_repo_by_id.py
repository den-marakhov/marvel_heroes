import pytest
from unittest.mock import AsyncMock, MagicMock

from src.domain.entities.hero import HeroEntity

from src.application.usecases.repo.get_hero_by_id_from_repo import GetHeroFromRepoUseCase
from src.application.dtos.hero import HeroDTO
from src.application.exceptions import HeroNotFoundError


class TestGetHeroFromRepoByIdUseCase:

	@pytest.fixture
	def mock_get_hero_from_cache_usecase(self) -> AsyncMock:
		return AsyncMock()
	
	@pytest.fixture
	def mock_save_hero_to_cache_usecase(self) -> AsyncMock:
		return AsyncMock()
	
	@pytest.fixture
	def get_hero_from_repo_by_id(
		self,
		mock_uow: AsyncMock,
		mock_mapper: MagicMock,
		mock_get_hero_from_cache_usecase: AsyncMock,
		mock_save_hero_to_cache_usecase: AsyncMock
	) -> GetHeroFromRepoUseCase:
		return GetHeroFromRepoUseCase(
			uow=mock_uow,
			mapper=mock_mapper,
			get_hero_from_cache_usecase=mock_get_hero_from_cache_usecase,
			save_hero_to_cache_usecase=mock_save_hero_to_cache_usecase
		)
	
	@pytest.mark.asyncio
	async def test_retrieve_hero_from_cache(
		self,
		mock_uow: AsyncMock,
		get_hero_from_repo_by_id: GetHeroFromRepoUseCase,
		mock_get_hero_from_cache_usecase: AsyncMock,
		mock_save_hero_to_cache_usecase: AsyncMock,
		sample_hero_dto: HeroDTO
	):
		hero_id = sample_hero_dto.hero_id
		hero_id_str = str(hero_id)
		mock_get_hero_from_cache_usecase.return_value = sample_hero_dto

		result = await get_hero_from_repo_by_id(hero_id=hero_id)

		assert result == sample_hero_dto
		mock_get_hero_from_cache_usecase.assert_called_once_with(hero_id_str)
		mock_uow.repository.get_hero_by_id.assert_not_called()
		mock_save_hero_to_cache_usecase.assert_not_called()
	
	@pytest.mark.asyncio
	async def test_retrieve_hero_from_repo(
		self,
		mock_uow: AsyncMock,
		mock_mapper: MagicMock,
		get_hero_from_repo_by_id: GetHeroFromRepoUseCase,
		mock_get_hero_from_cache_usecase: AsyncMock,
		mock_save_hero_to_cache_usecase: AsyncMock,
		sample_hero_dto: HeroDTO,
		sample_hero_entity: HeroEntity
	):
		
		mock_get_hero_from_cache_usecase.return_value = None
		mock_uow.repository.get_hero_by_id.return_value = sample_hero_entity

		mock_mapper.to_dto.return_value = sample_hero_dto
		
		hero_id = sample_hero_entity.hero_id
		hero_id_str = str(hero_id)
		result = await get_hero_from_repo_by_id(hero_id=hero_id)

		assert result == sample_hero_dto

		mock_get_hero_from_cache_usecase.assert_called_once_with(hero_id_str)
		mock_uow.repository.get_hero_by_id.assert_called_once_with(hero_id=hero_id)
		mock_mapper.to_dto.assert_called_once_with(sample_hero_entity)
		mock_save_hero_to_cache_usecase.assert_called_once_with(
			hero_id_str,
			sample_hero_dto
		)

	@pytest.mark.asyncio
	async def test_hero_not_found_in_repo(
		self,
		mock_uow: AsyncMock,
		get_hero_from_repo_by_id: GetHeroFromRepoUseCase,
		mock_get_hero_from_cache_usecase: AsyncMock,
		mock_save_hero_to_cache_usecase: AsyncMock,
		sample_hero_dto: HeroDTO
	):
		hero_id = sample_hero_dto.hero_id
		hero_id_str = str(hero_id)

		mock_get_hero_from_cache_usecase.return_value = None
		mock_uow.repository.get_hero_by_id.return_value = None

		with pytest.raises(HeroNotFoundError):
			await get_hero_from_repo_by_id(hero_id=hero_id)

		mock_get_hero_from_cache_usecase.assert_called_once_with(hero_id_str)
		mock_uow.repository.get_hero_by_id.assert_called_once_with(
			hero_id=hero_id
		)
		mock_save_hero_to_cache_usecase.assert_not_called()





		
