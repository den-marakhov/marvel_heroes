from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from src.application.dtos.token import TokenPayload
from src.application.exceptions.user import InvalidCredentialsError
from src.application.usecases.users.tokens.verify_user_session_tokens import (
    VerifyUserSessionTokensUseCase,
)


def _payload(
    *,
    user_id: UUID | None = None,
    session_id: UUID | None = None,
    jti: str = "access-jti",
    token_type: str = "access",
) -> TokenPayload:
    return TokenPayload(
        user_id=user_id or uuid4(),
        session_id=session_id or uuid4(),
        jti=jti,
        token_type=token_type,  # type: ignore[arg-type]
        expires_in=900,
    )


class TestVerifyUserSessionTokensUseCase:
    @pytest.fixture
    def mock_session_token_repository(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def mock_rehydrate_user_session_tokens_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def verify_user_session_tokens(
        self,
        mock_session_token_repository: AsyncMock,
        mock_rehydrate_user_session_tokens_usecase: AsyncMock,
    ) -> VerifyUserSessionTokensUseCase:
        return VerifyUserSessionTokensUseCase(
            session_token_repository=mock_session_token_repository,
            rehydrate_user_session_tokens_usecase=(
                mock_rehydrate_user_session_tokens_usecase
            ),
        )

    @pytest.mark.asyncio
    async def test_skips_rehydrate_when_access_jti_matches(
        self,
        verify_user_session_tokens: VerifyUserSessionTokensUseCase,
        mock_session_token_repository: AsyncMock,
        mock_rehydrate_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        payload = _payload()
        mock_session_token_repository.get_access_token_jti.return_value = payload.jti

        await verify_user_session_tokens(payload)

        mock_session_token_repository.get_access_token_jti.assert_awaited_once_with(
            payload.session_id
        )
        mock_rehydrate_user_session_tokens_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_skips_rehydrate_when_refresh_jti_matches(
        self,
        verify_user_session_tokens: VerifyUserSessionTokensUseCase,
        mock_session_token_repository: AsyncMock,
        mock_rehydrate_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        payload = _payload(jti="refresh-jti", token_type="refresh")
        mock_session_token_repository.get_refresh_token_jti.return_value = payload.jti

        await verify_user_session_tokens(payload)

        mock_session_token_repository.get_refresh_token_jti.assert_awaited_once_with(
            payload.session_id
        )
        mock_rehydrate_user_session_tokens_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_rehydrates_on_access_miss(
        self,
        verify_user_session_tokens: VerifyUserSessionTokensUseCase,
        mock_session_token_repository: AsyncMock,
        mock_rehydrate_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        payload = _payload()
        mock_session_token_repository.get_access_token_jti.return_value = None

        await verify_user_session_tokens(payload)

        mock_rehydrate_user_session_tokens_usecase.assert_awaited_once_with(payload)

    @pytest.mark.asyncio
    async def test_rehydrates_on_access_jti_mismatch(
        self,
        verify_user_session_tokens: VerifyUserSessionTokensUseCase,
        mock_session_token_repository: AsyncMock,
        mock_rehydrate_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        payload = _payload()
        mock_session_token_repository.get_access_token_jti.return_value = "rotated-access-jti"

        await verify_user_session_tokens(payload)

        mock_rehydrate_user_session_tokens_usecase.assert_awaited_once_with(payload)

    @pytest.mark.asyncio
    async def test_raises_when_miss_and_rehydrate_fails(
        self,
        verify_user_session_tokens: VerifyUserSessionTokensUseCase,
        mock_session_token_repository: AsyncMock,
        mock_rehydrate_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        payload = _payload()
        mock_session_token_repository.get_access_token_jti.return_value = None
        mock_rehydrate_user_session_tokens_usecase.side_effect = (
            InvalidCredentialsError("Authentication required")
        )

        with pytest.raises(InvalidCredentialsError):
            await verify_user_session_tokens(payload)

        mock_rehydrate_user_session_tokens_usecase.assert_awaited_once_with(payload)
