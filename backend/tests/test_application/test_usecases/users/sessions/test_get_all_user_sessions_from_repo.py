from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.mappers.user_session import UserSessionDtoEntityMapper
from src.application.usecases.users.sessions.get_all_user_sessions_from_repo import (
    GetAllUserSessionsFromRepoUseCase,
)
from src.domain.entities.user_session import UserSessionEntity


def _user_session(*, user_id):
    now = datetime.now(UTC)
    return UserSessionEntity(
        session_id=uuid4(),
        user_id=user_id,
        refresh_jti="refresh-jti",
        access_jti="access-jti",
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        expires_at=now + timedelta(days=30),
        created_at=now,
        last_seen_at=now,
    )


class TestGetAllUserSessionsFromRepoUseCase:
    @pytest.fixture
    def mock_uow(self) -> AsyncMock:
        uow = AsyncMock()
        uow.user_sessions = AsyncMock()
        return uow

    @pytest.fixture
    def get_all_user_sessions_from_repo(
        self, mock_uow: AsyncMock
    ) -> GetAllUserSessionsFromRepoUseCase:
        return GetAllUserSessionsFromRepoUseCase(
            uow=mock_uow,
            mapper=UserSessionDtoEntityMapper(),
        )

    @pytest.mark.asyncio
    async def test_retrieve_all_user_sessions_from_repo(
        self,
        get_all_user_sessions_from_repo: GetAllUserSessionsFromRepoUseCase,
        mock_uow: AsyncMock,
    ) -> None:
        first_user_id = uuid4()
        second_user_id = uuid4()
        user_session_entities = [
            _user_session(user_id=first_user_id),
            _user_session(user_id=second_user_id),
        ]
        mock_uow.user_sessions.get_all_user_sessions.return_value = (
            user_session_entities
        )

        result = await get_all_user_sessions_from_repo()

        assert len(result) == 2
        assert result[0].user_id == first_user_id
        assert result[1].user_id == second_user_id
        mock_uow.user_sessions.get_all_user_sessions.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_retrieve_empty_user_sessions_from_repo(
        self,
        get_all_user_sessions_from_repo: GetAllUserSessionsFromRepoUseCase,
        mock_uow: AsyncMock,
    ) -> None:
        mock_uow.user_sessions.get_all_user_sessions.return_value = []

        result = await get_all_user_sessions_from_repo()

        assert result == []
