from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.application.dtos.user import UserDTO
from src.application.exceptions.user import UserNotFoundError
from src.application.usecases.users.repo.get_user_by_email_from_repo import (
    GetUserByEmailFromRepoUseCase,
)
from src.domain.constants import ADMIN_ROLE
from src.domain.entities.user import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.role import Role
from src.domain.value_objects.user_name import UserName


def _user_entity() -> UserEntity:
    return UserEntity(
        user_id=uuid4(),
        email=Email(value="admin@marvel.local"),
        name=UserName(value="Admin"),
        password_hash="hashed-password",
        role=Role(value=ADMIN_ROLE),
    )


def _user_dto(user_id=None) -> UserDTO:
    return UserDTO(
        user_id=user_id or uuid4(),
        email="admin@marvel.local",
        name="Admin",
        role=ADMIN_ROLE,
        password_hash="hashed-password",
    )


class TestGetUserByEmailFromRepoUseCase:
    @pytest.fixture
    def mock_mapper(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def mock_get_user_by_email_from_cache_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def mock_save_user_to_cache_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def get_user_by_email_from_repo_usecase(
        self,
        mock_uow: AsyncMock,
        mock_mapper: MagicMock,
        mock_get_user_by_email_from_cache_usecase: AsyncMock,
        mock_save_user_to_cache_usecase: AsyncMock,
    ) -> GetUserByEmailFromRepoUseCase:
        return GetUserByEmailFromRepoUseCase(
            uow=mock_uow,
            mapper=mock_mapper,
            get_user_by_email_from_cache_usecase=mock_get_user_by_email_from_cache_usecase,
            save_user_to_cache_usecase=mock_save_user_to_cache_usecase,
        )

    @pytest.mark.asyncio
    async def test_retrieve_user_from_cache(
        self,
        mock_uow: AsyncMock,
        get_user_by_email_from_repo_usecase: GetUserByEmailFromRepoUseCase,
        mock_get_user_by_email_from_cache_usecase: AsyncMock,
        mock_save_user_to_cache_usecase: AsyncMock,
    ):
        user_dto = _user_dto()
        mock_get_user_by_email_from_cache_usecase.return_value = user_dto

        result = await get_user_by_email_from_repo_usecase("admin@marvel.local")

        assert result == user_dto
        mock_get_user_by_email_from_cache_usecase.assert_awaited_once_with(
            "admin@marvel.local"
        )
        mock_uow.users.get_by_email.assert_not_called()
        mock_save_user_to_cache_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_retrieve_user_from_repo(
        self,
        mock_uow: AsyncMock,
        mock_mapper: MagicMock,
        get_user_by_email_from_repo_usecase: GetUserByEmailFromRepoUseCase,
        mock_get_user_by_email_from_cache_usecase: AsyncMock,
        mock_save_user_to_cache_usecase: AsyncMock,
    ):
        user_entity = _user_entity()
        user_dto = _user_dto(user_id=user_entity.user_id)
        mock_get_user_by_email_from_cache_usecase.return_value = None
        mock_uow.users.get_by_email.return_value = user_entity
        mock_mapper.to_dto.return_value = user_dto

        result = await get_user_by_email_from_repo_usecase("admin@marvel.local")

        assert result == user_dto
        mock_get_user_by_email_from_cache_usecase.assert_awaited_once_with(
            "admin@marvel.local"
        )
        mock_uow.users.get_by_email.assert_awaited_once_with("admin@marvel.local")
        mock_mapper.to_dto.assert_called_once_with(user_entity)
        mock_save_user_to_cache_usecase.assert_awaited_once_with(
            str(user_entity.user_id), user_dto
        )

    @pytest.mark.asyncio
    async def test_raises_when_missing(
        self,
        mock_uow: AsyncMock,
        get_user_by_email_from_repo_usecase: GetUserByEmailFromRepoUseCase,
        mock_get_user_by_email_from_cache_usecase: AsyncMock,
        mock_save_user_to_cache_usecase: AsyncMock,
    ):
        mock_get_user_by_email_from_cache_usecase.return_value = None
        mock_uow.users.get_by_email.return_value = None

        with pytest.raises(UserNotFoundError):
            await get_user_by_email_from_repo_usecase("admin@marvel.local")

        mock_save_user_to_cache_usecase.assert_not_called()
