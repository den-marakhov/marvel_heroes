from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.dtos.user import CreateUserDTO, UserDTO
from src.application.exceptions.user import UserAlreadyExistsError
from src.application.usecases.users.seed_admin import SeedAdminUseCase
from src.domain.constants import ADMIN_ROLE


def _admin_dto() -> UserDTO:
    return UserDTO(
        user_id=uuid4(),
        email="admin@marvel.local",
        name="Admin",
        role=ADMIN_ROLE,
        password_hash="hashed-password",
    )


def _create_dto() -> CreateUserDTO:
    return CreateUserDTO(
        email="admin@marvel.local",
        name="Admin",
        role=ADMIN_ROLE,
        password_hash="hashed-password",
    )


class TestSeedAdminUseCase:
    @pytest.fixture
    def mock_create_user_in_repo_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def seed_admin_usecase(
        self,
        mock_create_user_in_repo_usecase: AsyncMock,
    ) -> SeedAdminUseCase:
        return SeedAdminUseCase(
            create_user_in_repo_usecase=mock_create_user_in_repo_usecase,
        )

    @pytest.mark.asyncio
    async def test_seeds_admin(
        self,
        seed_admin_usecase: SeedAdminUseCase,
        mock_create_user_in_repo_usecase: AsyncMock,
    ):
        create_dto = _create_dto()
        mock_create_user_in_repo_usecase.return_value = _admin_dto()

        await seed_admin_usecase(create_dto)

        mock_create_user_in_repo_usecase.assert_awaited_once_with(create_dto)

    @pytest.mark.asyncio
    async def test_skips_when_admin_exists(
        self,
        seed_admin_usecase: SeedAdminUseCase,
        mock_create_user_in_repo_usecase: AsyncMock,
    ):
        mock_create_user_in_repo_usecase.side_effect = UserAlreadyExistsError(
            "User 'admin@marvel.local' already exists in database"
        )

        await seed_admin_usecase(_create_dto())

        mock_create_user_in_repo_usecase.assert_awaited_once()
