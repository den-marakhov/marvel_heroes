from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
	AsyncEngine,
	AsyncSession,
	create_async_engine,
	async_sessionmaker
)

import pytest

from unittest.mock import AsyncMock, MagicMock

from src.domain.entities.hero import HeroEntity

from src.application.mappers import DtoEntityMapperProtocol
from src.application.interfaces.cache import CacheProtocol
from src.application.dtos.hero import HeroDTO

from src.infrastructures.mappers.hero import SerializationMapperProtocol

from tests.test_infrastructure.test_db.models.test_hero_model import TestBaseModel

from tests.factories import HeroDTOFactory, HeroEntityFactory


@pytest.fixture(scope="session")
def anyio_backend() -> str:
	return "asyncio"


@pytest.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
	engine = create_async_engine(
		"sqlite+aiosqlite:///:memory:",
		echo=False,
		connect_args={"check_same_thread": False},
	)
	yield engine
	await engine.dispose()


@pytest.fixture
async def test_session(
	test_engine: AsyncEngine
	) -> AsyncGenerator[AsyncSession, None]:
	async with test_engine.begin() as conn:
		await TestBaseModel.metadata.create_all(conn)

	async_session = async_sessionmaker(
		bind=test_engine,
		class_=AsyncSession,
		expire_on_commit=False
	)

	async with async_session() as session:
		yield session
		await session.rollback()


@pytest.fixture
def mock_uow() -> AsyncMock:
	return AsyncMock()

@pytest.fixture
def mock_mapper() -> MagicMock:
	return MagicMock(spec=DtoEntityMapperProtocol)

@pytest.fixture
def mock_cache_client() -> AsyncMock:
	return AsyncMock(spec=CacheProtocol)

@pytest.fixture
def mock_serialization_mapper() -> MagicMock:
	return MagicMock(spec=SerializationMapperProtocol)

@pytest.fixture
def sample_hero_dto() -> HeroDTO:
	return HeroDTOFactory.build()

@pytest.fixture
def sample_hero_entity() -> HeroEntity:
	return HeroEntityFactory.build()
