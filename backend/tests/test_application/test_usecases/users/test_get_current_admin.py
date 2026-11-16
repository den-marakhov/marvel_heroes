from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.dtos.user import UserDTO
from src.application.exceptions.user import AccessDeniedError
from src.application.usecases.users.get_current_admin import GetCurrentAdminUseCase
from src.domain.constants import ADMIN_ROLE


def _user(*, role: str = ADMIN_ROLE) -> UserDTO:
    return UserDTO(
        user_id=uuid4(),
        email="admin@marvel.local",
        name="Admin",
        role=role,
        password_hash="hashed-password",
    )


class TestGetCurrentAdminUseCase:
    @pytest.fixture
    def mock_get_current_user_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def get_current_admin_usecase(
        self,
        mock_get_current_user_usecase: AsyncMock,
    ) -> GetCurrentAdminUseCase:
        return GetCurrentAdminUseCase(
            get_current_user_usecase=mock_get_current_user_usecase,
        )

    @pytest.mark.asyncio
    async def test_returns_admin(
        self,
        get_current_admin_usecase: GetCurrentAdminUseCase,
        mock_get_current_user_usecase: AsyncMock,
    ):
        admin = _user()
        mock_get_current_user_usecase.return_value = admin

        result = await get_current_admin_usecase(access_token="access-jwt")

        assert result is admin
        mock_get_current_user_usecase.assert_awaited_once_with("access-jwt")

    @pytest.mark.asyncio
    async def test_non_admin_denied(
        self,
        get_current_admin_usecase: GetCurrentAdminUseCase,
        mock_get_current_user_usecase: AsyncMock,
    ):
        mock_get_current_user_usecase.return_value = _user(role="user")

        with pytest.raises(AccessDeniedError):
            await get_current_admin_usecase(access_token="access-jwt")
