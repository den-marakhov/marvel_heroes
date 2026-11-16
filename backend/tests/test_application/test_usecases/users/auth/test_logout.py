from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest

from src.application.dtos.token import TokenPayload
from src.application.exceptions.user import InvalidCredentialsError, InvalidTokenError
from src.application.usecases.users.auth.logout import LogoutUseCase
from src.domain.entities.user_session import UserSessionEntity


def _payload(
    *,
    user_id: UUID,
    session_id: UUID,
    jti: str,
    token_type: str,
    expires_in: int = 2_592_000,
) -> TokenPayload:
    return TokenPayload(
        user_id=user_id,
        session_id=session_id,
        jti=jti,
        token_type=token_type,  # type: ignore[arg-type]
        expires_in=expires_in,
    )


def _user_session(*, user_id: UUID, session_id: UUID) -> UserSessionEntity:
    now = datetime.now(UTC)
    return UserSessionEntity(
        session_id=session_id,
        user_id=user_id,
        refresh_jti="refresh-jti",
        access_jti="access-jti",
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        expires_at=now + timedelta(days=30),
        created_at=now,
        last_seen_at=now,
    )


class TestLogoutUseCase:
    @pytest.fixture
    def mock_token_service(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def mock_uow(self) -> AsyncMock:
        uow = AsyncMock()
        uow.user_sessions = AsyncMock()
        return uow

    @pytest.fixture
    def mock_verify_user_session_tokens_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def mock_delete_user_session_tokens_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def logout_usecase(
        self,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
        mock_uow: AsyncMock,
    ) -> LogoutUseCase:
        return LogoutUseCase(
            token_service=mock_token_service,
            verify_user_session_tokens_usecase=(
                mock_verify_user_session_tokens_usecase
            ),
            delete_user_session_tokens_usecase=(
                mock_delete_user_session_tokens_usecase
            ),
            uow=mock_uow,
        )

    @pytest.mark.asyncio
    async def test_logout_success(
        self,
        logout_usecase: LogoutUseCase,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
        mock_uow: AsyncMock,
    ):
        user_id = uuid4()
        session_id = uuid4()
        payload = _payload(
            user_id=user_id,
            session_id=session_id,
            jti="refresh-jti",
            token_type="refresh",
        )
        mock_token_service.decode_token.return_value = payload
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user_id, session_id=session_id
        )

        await logout_usecase(refresh_token="refresh-jwt")

        mock_verify_user_session_tokens_usecase.assert_awaited_once_with(payload)
        mock_uow.user_sessions.revoke_session.assert_awaited_once_with(session_id)
        mock_delete_user_session_tokens_usecase.assert_awaited_once_with(
            session_id=session_id, user_id=user_id
        )

    @pytest.mark.asyncio
    async def test_logout_without_db_session_still_clears_redis(
        self,
        logout_usecase: LogoutUseCase,
        mock_token_service: MagicMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
        mock_uow: AsyncMock,
    ):
        user_id = uuid4()
        session_id = uuid4()
        mock_token_service.decode_token.return_value = _payload(
            user_id=user_id,
            session_id=session_id,
            jti="refresh-jti",
            token_type="refresh",
        )
        mock_uow.user_sessions.get_user_session_by_id.return_value = None

        await logout_usecase(refresh_token="refresh-jwt")

        mock_uow.user_sessions.revoke_session.assert_not_called()
        mock_delete_user_session_tokens_usecase.assert_awaited_once_with(
            session_id=session_id, user_id=user_id
        )

    @pytest.mark.asyncio
    async def test_logout_invalid_token(
        self,
        logout_usecase: LogoutUseCase,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
    ):
        mock_token_service.decode_token.side_effect = InvalidTokenError("bad jwt")

        with pytest.raises(InvalidCredentialsError):
            await logout_usecase(refresh_token="broken-jwt")

        mock_verify_user_session_tokens_usecase.assert_not_called()
        mock_delete_user_session_tokens_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_logout_access_token_rejected(
        self,
        logout_usecase: LogoutUseCase,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
    ):
        mock_token_service.decode_token.return_value = _payload(
            user_id=uuid4(),
            session_id=uuid4(),
            jti="access-jti",
            token_type="access",
            expires_in=900,
        )

        with pytest.raises(InvalidCredentialsError):
            await logout_usecase(refresh_token="access-jwt")

        mock_verify_user_session_tokens_usecase.assert_not_called()
        mock_delete_user_session_tokens_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_logout_when_verify_fails(
        self,
        logout_usecase: LogoutUseCase,
        mock_token_service: MagicMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
    ):
        mock_token_service.decode_token.return_value = _payload(
            user_id=uuid4(),
            session_id=uuid4(),
            jti="revoked-jti",
            token_type="refresh",
        )
        mock_verify_user_session_tokens_usecase.side_effect = InvalidCredentialsError(
            "Authentication required"
        )

        with pytest.raises(InvalidCredentialsError):
            await logout_usecase(refresh_token="revoked-refresh-jwt")

        mock_verify_user_session_tokens_usecase.assert_awaited_once()
        mock_delete_user_session_tokens_usecase.assert_not_called()
