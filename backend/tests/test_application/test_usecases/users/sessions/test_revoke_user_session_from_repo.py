from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.exceptions.user_session import UserSessionNotFoundError
from src.application.usecases.users.sessions.revoke_user_session_from_repo import (
    RevokeUserSessionFromRepoUseCase,
)
from src.domain.entities.user_session import UserSessionEntity


def _user_session(*, user_id, session_id, revoked_at=None):
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
        revoked_at=revoked_at,
    )


class TestRevokeUserSessionFromRepoUseCase:
    @pytest.fixture
    def mock_uow(self) -> AsyncMock:
        uow = AsyncMock()
        uow.user_sessions = AsyncMock()
        return uow

    @pytest.fixture
    def mock_delete_user_session_tokens_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def revoke_user_session_from_repo(
        self,
        mock_uow: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
    ) -> RevokeUserSessionFromRepoUseCase:
        return RevokeUserSessionFromRepoUseCase(
            uow=mock_uow,
            delete_user_session_tokens_usecase=(
                mock_delete_user_session_tokens_usecase
            ),
        )

    @pytest.mark.asyncio
    async def test_revokes_own_session_from_repo(
        self,
        revoke_user_session_from_repo: RevokeUserSessionFromRepoUseCase,
        mock_uow: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        user_id = uuid4()
        session_id = uuid4()
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user_id, session_id=session_id
        )

        await revoke_user_session_from_repo(user_id, session_id)

        mock_uow.user_sessions.revoke_session.assert_awaited_once_with(session_id)
        mock_delete_user_session_tokens_usecase.assert_awaited_once_with(
            session_id=session_id, user_id=user_id
        )

    @pytest.mark.asyncio
    async def test_missing_session(
        self,
        revoke_user_session_from_repo: RevokeUserSessionFromRepoUseCase,
        mock_uow: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        mock_uow.user_sessions.get_user_session_by_id.return_value = None

        with pytest.raises(UserSessionNotFoundError):
            await revoke_user_session_from_repo(uuid4(), uuid4())

        mock_delete_user_session_tokens_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_foreign_session(
        self,
        revoke_user_session_from_repo: RevokeUserSessionFromRepoUseCase,
        mock_uow: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        session_id = uuid4()
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=uuid4(), session_id=session_id
        )

        with pytest.raises(UserSessionNotFoundError):
            await revoke_user_session_from_repo(uuid4(), session_id)

        mock_delete_user_session_tokens_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_already_revoked(
        self,
        revoke_user_session_from_repo: RevokeUserSessionFromRepoUseCase,
        mock_uow: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        user_id = uuid4()
        session_id = uuid4()
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=user_id,
            session_id=session_id,
            revoked_at=datetime.now(UTC),
        )

        with pytest.raises(UserSessionNotFoundError):
            await revoke_user_session_from_repo(user_id, session_id)

        mock_delete_user_session_tokens_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_revokes_any_session_when_user_id_is_omitted(
        self,
        revoke_user_session_from_repo: RevokeUserSessionFromRepoUseCase,
        mock_uow: AsyncMock,
        mock_delete_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        owner_id = uuid4()
        session_id = uuid4()
        mock_uow.user_sessions.get_user_session_by_id.return_value = _user_session(
            user_id=owner_id, session_id=session_id
        )

        await revoke_user_session_from_repo(None, session_id)

        mock_uow.user_sessions.revoke_session.assert_awaited_once_with(session_id)
        mock_delete_user_session_tokens_usecase.assert_awaited_once_with(
            session_id=session_id, user_id=owner_id
        )
