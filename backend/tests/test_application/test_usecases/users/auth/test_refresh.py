from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest

from src.application.dtos.token import AuthTokensDTO, TokenPayload
from src.application.exceptions.user import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
)
from src.application.usecases.users.auth.refresh import RefreshUseCase
from src.domain.constants import ADMIN_ROLE
from src.domain.entities.user import UserEntity
from src.domain.entities.user_session import UserSessionEntity
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


def _user_session(
    *,
    user_id: UUID,
    session_id: UUID,
    created_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> UserSessionEntity:
    now = datetime.now(UTC)
    created_at = created_at or now
    return UserSessionEntity(
        session_id=session_id,
        user_id=user_id,
        refresh_jti="old-refresh-jti",
        access_jti="old-access-jti",
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        expires_at=expires_at or created_at + timedelta(days=30),
        created_at=created_at,
        last_seen_at=created_at,
    )


class TestRefreshUseCase:
    @pytest.fixture
    def mock_token_service(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def mock_session_token_repository(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def mock_get_user_from_repo_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def mock_uow(self) -> AsyncMock:
        uow = AsyncMock()
        uow.user_sessions = AsyncMock()
        return uow

    @pytest.fixture
    def mock_verify_user_session_tokens_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def refresh_usecase(
        self,
        mock_get_user_from_repo_usecase: AsyncMock,
        mock_token_service: MagicMock,
        mock_session_token_repository: AsyncMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_uow: AsyncMock,
    ) -> RefreshUseCase:
        return RefreshUseCase(
            get_user_from_repo_usecase=mock_get_user_from_repo_usecase,
            token_service=mock_token_service,
            session_token_repository=mock_session_token_repository,
            verify_user_session_tokens_usecase=(
                mock_verify_user_session_tokens_usecase
            ),
            uow=mock_uow,
        )

    @pytest.mark.asyncio
    async def test_refresh_success(
        self,
        refresh_usecase: RefreshUseCase,
        mock_get_user_from_repo_usecase: AsyncMock,
        mock_token_service: MagicMock,
        mock_session_token_repository: AsyncMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_uow: AsyncMock,
    ):
        user = _user()
        session_id = uuid4()
        tokens = AuthTokensDTO(
            access_token="new-access-jwt",
            refresh_token="new-refresh-jwt",
            access_payload=_payload(
                user_id=user.user_id,
                session_id=session_id,
                jti="new-access-jti",
                token_type="access",
                expires_in=900,
            ),
            refresh_payload=_payload(
                user_id=user.user_id,
                session_id=session_id,
                jti="new-refresh-jti",
                token_type="refresh",
                expires_in=2_592_000,
            ),
        )
        mock_get_user_from_repo_usecase.return_value = user
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user.user_id, session_id=session_id
        )
        mock_token_service.decode_token.return_value = _payload(
            user_id=user.user_id,
            session_id=session_id,
            jti="old-refresh-jti",
            token_type="refresh",
            expires_in=2_592_000,
        )
        mock_token_service.create_token_pair.return_value = tokens

        result = await refresh_usecase(refresh_token="old-refresh-jwt")

        assert result is tokens
        mock_verify_user_session_tokens_usecase.assert_awaited_once()
        mock_get_user_from_repo_usecase.assert_awaited_once_with(user.user_id)
        mock_token_service.create_token_pair.assert_called_once_with(
            user.user_id, session_id
        )
        mock_uow.user_sessions.update_user_session.assert_awaited_once()
        updated = mock_uow.user_sessions.update_user_session.await_args.args[0]
        assert updated.access_jti == "new-access-jti"
        assert updated.refresh_jti == "new-refresh-jti"
        mock_session_token_repository.save_token_pair.assert_awaited_once_with(tokens)
        mock_session_token_repository.delete_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_refresh_invalid_token(
        self,
        refresh_usecase: RefreshUseCase,
        mock_token_service: MagicMock,
        mock_session_token_repository: AsyncMock,
    ):
        mock_token_service.decode_token.side_effect = InvalidTokenError("bad jwt")

        with pytest.raises(InvalidCredentialsError):
            await refresh_usecase(refresh_token="broken-jwt")

        mock_session_token_repository.save_token_pair.assert_not_called()

    @pytest.mark.asyncio
    async def test_refresh_access_token_rejected(
        self,
        refresh_usecase: RefreshUseCase,
        mock_token_service: MagicMock,
        mock_session_token_repository: AsyncMock,
    ):
        mock_token_service.decode_token.return_value = _payload(
            user_id=uuid4(),
            session_id=uuid4(),
            jti="access-jti",
            token_type="access",
        )

        with pytest.raises(InvalidCredentialsError):
            await refresh_usecase(refresh_token="access-jwt")

        mock_session_token_repository.save_token_pair.assert_not_called()

    @pytest.mark.asyncio
    async def test_refresh_revoked_token(
        self,
        refresh_usecase: RefreshUseCase,
        mock_get_user_from_repo_usecase: AsyncMock,
        mock_token_service: MagicMock,
        mock_session_token_repository: AsyncMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
    ):
        mock_token_service.decode_token.return_value = _payload(
            user_id=uuid4(),
            session_id=uuid4(),
            jti="revoked-jti",
            token_type="refresh",
            expires_in=2_592_000,
        )
        mock_verify_user_session_tokens_usecase.side_effect = InvalidCredentialsError(
            "Authentication required"
        )

        with pytest.raises(InvalidCredentialsError):
            await refresh_usecase(refresh_token="revoked-refresh-jwt")

        mock_get_user_from_repo_usecase.assert_not_called()
        mock_verify_user_session_tokens_usecase.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_refresh_missing_user_session(
        self,
        refresh_usecase: RefreshUseCase,
        mock_get_user_from_repo_usecase: AsyncMock,
        mock_token_service: MagicMock,
        mock_session_token_repository: AsyncMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
        mock_uow: AsyncMock,
    ):
        user = _user()
        session_id = uuid4()
        mock_get_user_from_repo_usecase.return_value = user
        mock_uow.user_sessions.get_user_session_by_id.return_value = None
        mock_token_service.decode_token.return_value = _payload(
            user_id=user.user_id,
            session_id=session_id,
            jti="old-refresh-jti",
            token_type="refresh",
            expires_in=2_592_000,
        )

        with pytest.raises(InvalidCredentialsError):
            await refresh_usecase(refresh_token="old-refresh-jwt")

        mock_token_service.create_token_pair.assert_not_called()
        mock_session_token_repository.save_token_pair.assert_not_called()

    @pytest.mark.asyncio
    async def test_refresh_expired_user_session(
        self,
        refresh_usecase: RefreshUseCase,
        mock_get_user_from_repo_usecase: AsyncMock,
        mock_token_service: MagicMock,
        mock_session_token_repository: AsyncMock,
        mock_uow: AsyncMock,
    ):
        user = _user()
        session_id = uuid4()
        now = datetime.now(UTC)
        mock_get_user_from_repo_usecase.return_value = user
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user.user_id,
            session_id=session_id,
            created_at=now - timedelta(days=30),
            expires_at=now - timedelta(seconds=1),
        )
        mock_token_service.decode_token.return_value = _payload(
            user_id=user.user_id,
            session_id=session_id,
            jti="old-refresh-jti",
            token_type="refresh",
            expires_in=2_592_000,
        )

        with pytest.raises(InvalidCredentialsError):
            await refresh_usecase(refresh_token="old-refresh-jwt")

        mock_token_service.create_token_pair.assert_not_called()
        mock_session_token_repository.save_token_pair.assert_not_called()

    @pytest.mark.asyncio
    async def test_refresh_user_not_found(
        self,
        refresh_usecase: RefreshUseCase,
        mock_get_user_from_repo_usecase: AsyncMock,
        mock_token_service: MagicMock,
        mock_session_token_repository: AsyncMock,
        mock_verify_user_session_tokens_usecase: AsyncMock,
    ):
        user_id = uuid4()
        mock_token_service.decode_token.return_value = _payload(
            user_id=user_id,
            session_id=uuid4(),
            jti="refresh-jti",
            token_type="refresh",
            expires_in=2_592_000,
        )
        mock_get_user_from_repo_usecase.side_effect = UserNotFoundError(
            f"User '{user_id}' has not been found in database"
        )

        with pytest.raises(InvalidCredentialsError):
            await refresh_usecase(refresh_token="refresh-jwt")

        mock_session_token_repository.save_token_pair.assert_not_called()
