from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest

from src.application.dtos.token import TokenPayload
from src.application.exceptions.user import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
)
from src.application.usecases.users.get_current_user import GetCurrentUserUseCase
from src.domain.constants import ADMIN_ROLE
from src.domain.entities.user import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.role import Role
from src.domain.value_objects.user_name import UserName


def _payload(
    *,
    user_id: UUID,
    session_id: UUID,
    jti: str,
    token_type: str,
    expires_in: int = 900,
) -> TokenPayload:
    return TokenPayload(
        user_id=user_id,
        session_id=session_id,
        jti=jti,
        token_type=token_type,  # type: ignore[arg-type]
        expires_in=expires_in,
    )


def _user() -> UserEntity:
    return UserEntity(
        user_id=uuid4(),
        email=Email(value="admin@marvel.local"),
        name=UserName(value="Admin"),
        password_hash="hashed-password",
        role=Role(value=ADMIN_ROLE),
    )


class TestGetCurrentUserUseCase:
    @pytest.fixture
    def mock_token_service(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def mock_get_user_from_repo_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def mock_verify_user_session_tokens_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def get_current_user_usecase(
        self,
        mock_get_user_from_repo_usecase: AsyncMock,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
    ) -> GetCurrentUserUseCase:
        return GetCurrentUserUseCase(
            get_user_from_repo_usecase=mock_get_user_from_repo_usecase,
            token_service=mock_token_service,
            verify_user_session_tokens_usecase=(
                mock_verify_user_session_tokens_usecase
            ),
        )

    @pytest.mark.asyncio
    async def test_returns_user(
        self,
        get_current_user_usecase: GetCurrentUserUseCase,
        mock_get_user_from_repo_usecase: AsyncMock,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
    ):
        user = _user()
        payload = _payload(
            user_id=user.user_id,
            session_id=uuid4(),
            jti="access-jti",
            token_type="access",
        )
        mock_token_service.decode_token.return_value = payload
        mock_get_user_from_repo_usecase.return_value = user

        result = await get_current_user_usecase(access_token="access-jwt")

        assert result is user
        mock_verify_user_session_tokens_usecase.assert_awaited_once_with(payload)
        mock_get_user_from_repo_usecase.assert_awaited_once_with(user.user_id)

    @pytest.mark.asyncio
    async def test_invalid_token(
        self,
        get_current_user_usecase: GetCurrentUserUseCase,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
    ):
        mock_token_service.decode_token.side_effect = InvalidTokenError("Invalid token")

        with pytest.raises(InvalidCredentialsError):
            await get_current_user_usecase(access_token="broken-jwt")

        mock_verify_user_session_tokens_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_refresh_token_rejected(
        self,
        get_current_user_usecase: GetCurrentUserUseCase,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
    ):
        mock_token_service.decode_token.return_value = _payload(
            user_id=uuid4(),
            session_id=uuid4(),
            jti="refresh-jti",
            token_type="refresh",
            expires_in=2_592_000,
        )

        with pytest.raises(InvalidCredentialsError):
            await get_current_user_usecase(access_token="refresh-jwt")

        mock_verify_user_session_tokens_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_revoked_access_token(
        self,
        get_current_user_usecase: GetCurrentUserUseCase,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_get_user_from_repo_usecase: AsyncMock,
    ):
        mock_token_service.decode_token.return_value = _payload(
            user_id=uuid4(),
            session_id=uuid4(),
            jti="access-jti",
            token_type="access",
        )
        mock_verify_user_session_tokens_usecase.side_effect = InvalidCredentialsError(
            "Authentication required"
        )

        with pytest.raises(InvalidCredentialsError):
            await get_current_user_usecase(access_token="access-jwt")

        mock_get_user_from_repo_usecase.assert_not_called()
        mock_verify_user_session_tokens_usecase.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_missing_user(
        self,
        get_current_user_usecase: GetCurrentUserUseCase,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_get_user_from_repo_usecase: AsyncMock,
    ):
        mock_token_service.decode_token.return_value = _payload(
            user_id=uuid4(),
            session_id=uuid4(),
            jti="access-jti",
            token_type="access",
        )
        mock_get_user_from_repo_usecase.side_effect = UserNotFoundError(
            "User has not been found in database"
        )

        with pytest.raises(InvalidCredentialsError):
            await get_current_user_usecase(access_token="access-jwt")
