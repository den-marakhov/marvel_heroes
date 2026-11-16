from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.application.dtos.user import CreateUserDTO, UserDTO
from src.application.exceptions.user import UserAlreadyExistsError
from src.application.usecases.users.repo.create_user_in_repo import (
    CreateUserInRepoUseCase,
)
from src.domain.constants import ADMIN_ROLE
from src.domain.entities.user import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.role import Role
from src.domain.value_objects.user_name import UserName
from src.infrastructures.db.exceptions import RepositoryConflictError


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


class TestCreateUserInRepoUseCase:
    @pytest.fixture
    def mock_mapper(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def mock_save_user_to_cache_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def create_user_in_repo_usecase(
        self,
        mock_uow: AsyncMock,
        mock_mapper: MagicMock,
        mock_save_user_to_cache_usecase: AsyncMock,
    ) -> CreateUserInRepoUseCase:
        return CreateUserInRepoUseCase(
            uow=mock_uow,
            mapper=mock_mapper,
            save_user_to_cache_usecase=mock_save_user_to_cache_usecase,
        )

    @pytest.mark.asyncio
    async def test_creates_user(
        self,
        mock_uow: AsyncMock,
        mock_mapper: MagicMock,
        create_user_in_repo_usecase: CreateUserInRepoUseCase,
        mock_save_user_to_cache_usecase: AsyncMock,
    ):
        user_entity = _user_entity()
        user_dto = _user_dto(user_id=user_entity.user_id)
        create_dto = CreateUserDTO(
            email="admin@marvel.local",
            name="Admin",
            role=ADMIN_ROLE,
            password_hash="hashed-password",
        )
        mock_uow.users.get_by_email.return_value = None
        mock_mapper.to_entity_from_create_dto.return_value = user_entity
        mock_mapper.to_dto.return_value = user_dto

        result = await create_user_in_repo_usecase(create_dto)

        assert result == user_dto
        mock_uow.users.get_by_email.assert_awaited_once_with(create_dto.email)
        mock_mapper.to_entity_from_create_dto.assert_called_once_with(create_dto)
        mock_uow.users.save.assert_awaited_once_with(user_entity)
        mock_mapper.to_dto.assert_called_once_with(user_entity)
        mock_save_user_to_cache_usecase.assert_awaited_once_with(
            str(user_entity.user_id), user_dto
        )

    @pytest.mark.asyncio
    async def test_raises_when_email_taken(
        self,
        mock_uow: AsyncMock,
        create_user_in_repo_usecase: CreateUserInRepoUseCase,
        mock_save_user_to_cache_usecase: AsyncMock,
    ):
        create_dto = CreateUserDTO(
            email="admin@marvel.local",
            name="Admin",
            role=ADMIN_ROLE,
            password_hash="hashed-password",
        )
        mock_uow.users.get_by_email.return_value = _user_entity()

        with pytest.raises(UserAlreadyExistsError):
            await create_user_in_repo_usecase(create_dto)

        mock_uow.users.save.assert_not_called()
        mock_save_user_to_cache_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_when_save_conflicts(
        self,
        mock_uow: AsyncMock,
        mock_mapper: MagicMock,
        create_user_in_repo_usecase: CreateUserInRepoUseCase,
        mock_save_user_to_cache_usecase: AsyncMock,
    ):
        create_dto = CreateUserDTO(
            email="admin@marvel.local",
            name="Admin",
            role=ADMIN_ROLE,
            password_hash="hashed-password",
        )
        mock_uow.users.get_by_email.return_value = None
        mock_mapper.to_entity_from_create_dto.return_value = _user_entity()
        mock_uow.users.save.side_effect = RepositoryConflictError("duplicate email")

        with pytest.raises(UserAlreadyExistsError):
            await create_user_in_repo_usecase(create_dto)

        mock_save_user_to_cache_usecase.assert_not_called()
