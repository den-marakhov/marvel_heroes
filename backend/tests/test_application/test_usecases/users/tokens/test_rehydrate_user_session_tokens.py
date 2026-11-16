from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from src.application.dtos.token import TokenPayload, UpdateUserSessionTokensDTO
from src.application.exceptions.user import InvalidCredentialsError
from src.application.mappers.user_session import UserSessionDtoEntityMapper
from src.application.usecases.users.tokens.rehydrate_user_session_tokens import (
    RehydrateUserSessionTokensUseCase,
)
from src.domain.entities.user_session import UserSessionEntity


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


def _user_session(
    *,
    user_id: UUID,
    session_id: UUID,
    access_jti: str = "access-jti",
    refresh_jti: str = "refresh-jti",
    revoked_at: datetime | None = None,
    expires_at: datetime | None = None,
    created_at: datetime | None = None,
) -> UserSessionEntity:
    now = datetime.now(UTC)
    created = created_at or now
    return UserSessionEntity(
        session_id=session_id,
        user_id=user_id,
        refresh_jti=refresh_jti,
        access_jti=access_jti,
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        expires_at=expires_at or (created + timedelta(days=30)),
        created_at=created,
        last_seen_at=created,
        revoked_at=revoked_at,
    )


class TestRehydrateUserSessionTokensUseCase:
    @pytest.fixture
    def mock_uow(self) -> AsyncMock:
        uow = AsyncMock()
        uow.user_sessions = AsyncMock()
        return uow

    @pytest.fixture
    def mock_session_token_repository(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def rehydrate_user_session_tokens(
        self, mock_uow: AsyncMock, mock_session_token_repository: AsyncMock
    ) -> RehydrateUserSessionTokensUseCase:
        return RehydrateUserSessionTokensUseCase(
            uow=mock_uow,
            session_token_repository=mock_session_token_repository,
            mapper=UserSessionDtoEntityMapper(),
        )

    @pytest.mark.asyncio
    async def test_rehydrates_access_token(
        self,
        rehydrate_user_session_tokens: RehydrateUserSessionTokensUseCase,
        mock_uow: AsyncMock,
        mock_session_token_repository: AsyncMock,
    ) -> None:
        user_id = uuid4()
        session_id = uuid4()
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user_id, session_id=session_id
        )

        await rehydrate_user_session_tokens(
            _payload(
                user_id=user_id,
                session_id=session_id,
                jti="access-jti",
                token_type="access",
                expires_in=400,
            )
        )

        update_user_session_tokens_dto = (
            mock_session_token_repository.update_session_tokens.await_args.args[0]
        )
        assert update_user_session_tokens_dto == UpdateUserSessionTokensDTO(
            session_id=session_id,
            user_id=user_id,
            access_jti="access-jti",
            refresh_jti="refresh-jti",
            access_ttl=400,
            refresh_ttl=update_user_session_tokens_dto.refresh_ttl,
        )
        assert update_user_session_tokens_dto.refresh_ttl > 1

    @pytest.mark.asyncio
    async def test_rehydrates_refresh_token(
        self,
        rehydrate_user_session_tokens: RehydrateUserSessionTokensUseCase,
        mock_uow: AsyncMock,
        mock_session_token_repository: AsyncMock,
    ) -> None:
        user_id = uuid4()
        session_id = uuid4()
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user_id, session_id=session_id
        )

        await rehydrate_user_session_tokens(
            _payload(
                user_id=user_id,
                session_id=session_id,
                jti="refresh-jti",
                token_type="refresh",
                expires_in=2_592_000,
            )
        )

        update_user_session_tokens_dto = (
            mock_session_token_repository.update_session_tokens.await_args.args[0]
        )
        assert update_user_session_tokens_dto.access_ttl == 1
        assert update_user_session_tokens_dto.refresh_ttl == 2_592_000

    @pytest.mark.asyncio
    async def test_missing_session(
        self,
        rehydrate_user_session_tokens: RehydrateUserSessionTokensUseCase,
        mock_uow: AsyncMock,
        mock_session_token_repository: AsyncMock,
    ) -> None:
        mock_uow.user_sessions.get_user_session_by_id.return_value = None

        with pytest.raises(InvalidCredentialsError):
            await rehydrate_user_session_tokens(
                _payload(
                    user_id=uuid4(),
                    session_id=uuid4(),
                    jti="access-jti",
                    token_type="access",
                )
            )

        mock_session_token_repository.update_session_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_revoked_session(
        self,
        rehydrate_user_session_tokens: RehydrateUserSessionTokensUseCase,
        mock_uow: AsyncMock,
        mock_session_token_repository: AsyncMock,
    ) -> None:
        user_id = uuid4()
        session_id = uuid4()
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user_id,
            session_id=session_id,
            revoked_at=datetime.now(UTC),
        )

        with pytest.raises(InvalidCredentialsError):
            await rehydrate_user_session_tokens(
                _payload(
                    user_id=user_id,
                    session_id=session_id,
                    jti="access-jti",
                    token_type="access",
                )
            )

        mock_session_token_repository.update_session_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_jti_mismatch(
        self,
        rehydrate_user_session_tokens: RehydrateUserSessionTokensUseCase,
        mock_uow: AsyncMock,
        mock_session_token_repository: AsyncMock,
    ) -> None:
        user_id = uuid4()
        session_id = uuid4()
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user_id, session_id=session_id
        )

        with pytest.raises(InvalidCredentialsError):
            await rehydrate_user_session_tokens(
                _payload(
                    user_id=user_id,
                    session_id=session_id,
                    jti="old-access-jti",
                    token_type="access",
                )
            )

        mock_session_token_repository.update_session_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_foreign_session(
        self,
        rehydrate_user_session_tokens: RehydrateUserSessionTokensUseCase,
        mock_uow: AsyncMock,
        mock_session_token_repository: AsyncMock,
    ) -> None:
        session_id = uuid4()
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=uuid4(), session_id=session_id
        )

        with pytest.raises(InvalidCredentialsError):
            await rehydrate_user_session_tokens(
                _payload(
                    user_id=uuid4(),
                    session_id=session_id,
                    jti="access-jti",
                    token_type="access",
                )
            )

        mock_session_token_repository.update_session_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_expired_session(
        self,
        rehydrate_user_session_tokens: RehydrateUserSessionTokensUseCase,
        mock_uow: AsyncMock,
        mock_session_token_repository: AsyncMock,
    ) -> None:
        user_id = uuid4()
        session_id = uuid4()
        now = datetime.now(UTC)
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user_id,
            session_id=session_id,
            created_at=now - timedelta(days=2),
            expires_at=now - timedelta(seconds=1),
        )

        with pytest.raises(InvalidCredentialsError):
            await rehydrate_user_session_tokens(
                _payload(
                    user_id=user_id,
                    session_id=session_id,
                    jti="access-jti",
                    token_type="access",
                )
            )

        mock_session_token_repository.update_session_tokens.assert_not_called()
