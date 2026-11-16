from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.usecases.users.sessions.revoke_all_user_sessions_from_repo import (
    RevokeAllUserSessionsFromRepoUseCase,
)


class TestRevokeAllUserSessionsFromRepoUseCase:
    @pytest.fixture
    def mock_uow(self) -> AsyncMock:
        uow = AsyncMock()
        uow.user_sessions = AsyncMock()
        return uow

    @pytest.fixture
    def mock_delete_all_user_session_tokens_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def revoke_all_user_sessions_from_repo(
        self,
        mock_uow: AsyncMock,
        mock_delete_all_user_session_tokens_usecase: AsyncMock,
    ) -> RevokeAllUserSessionsFromRepoUseCase:
        return RevokeAllUserSessionsFromRepoUseCase(
            uow=mock_uow,
            delete_all_user_session_tokens_usecase=(
                mock_delete_all_user_session_tokens_usecase
            ),
        )

    @pytest.mark.asyncio
    async def test_revokes_all_sessions_from_repo(
        self,
        revoke_all_user_sessions_from_repo: RevokeAllUserSessionsFromRepoUseCase,
        mock_uow: AsyncMock,
        mock_delete_all_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        user_id = uuid4()

        await revoke_all_user_sessions_from_repo(user_id)

        mock_uow.user_sessions.revoke_all_user_sessions.assert_awaited_once_with(
            user_id
        )
        mock_delete_all_user_session_tokens_usecase.assert_awaited_once_with(user_id)

    @pytest.mark.asyncio
    async def test_does_not_delete_tokens_when_repo_fails(
        self,
        revoke_all_user_sessions_from_repo: RevokeAllUserSessionsFromRepoUseCase,
        mock_uow: AsyncMock,
        mock_delete_all_user_session_tokens_usecase: AsyncMock,
    ) -> None:
        mock_uow.user_sessions.revoke_all_user_sessions.side_effect = RuntimeError(
            "db down"
        )

        with pytest.raises(RuntimeError):
            await revoke_all_user_sessions_from_repo(uuid4())

        mock_delete_all_user_session_tokens_usecase.assert_not_called()
