from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.mappers.user_session import UserSessionDtoEntityMapper
from src.application.usecases.users.sessions.get_user_sessions_from_repo import (
    GetUserSessionsFromRepoUseCase,
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


class TestGetUserSessionsFromRepoUseCase:
    @pytest.fixture
    def mock_uow(self) -> AsyncMock:
        uow = AsyncMock()
        uow.user_sessions = AsyncMock()
        return uow

    @pytest.fixture
    def get_user_sessions_from_repo(
        self, mock_uow: AsyncMock
    ) -> GetUserSessionsFromRepoUseCase:
        return GetUserSessionsFromRepoUseCase(
            uow=mock_uow,
            mapper=UserSessionDtoEntityMapper(),
        )

    @pytest.mark.asyncio
    async def test_retrieve_user_sessions_from_repo(
        self,
        get_user_sessions_from_repo: GetUserSessionsFromRepoUseCase,
        mock_uow: AsyncMock,
    ) -> None:
        user_id = uuid4()
        user_session_entities = [
            _user_session(user_id=user_id),
            _user_session(user_id=user_id),
        ]
        mock_uow.user_sessions.get_user_sessions.return_value = user_session_entities

        result = await get_user_sessions_from_repo(user_id)

        assert len(result) == 2
        assert result[0].session_id == user_session_entities[0].session_id
        assert result[1].ip == "127.0.0.1"
        mock_uow.user_sessions.get_user_sessions.assert_awaited_once_with(
            user_id=user_id
        )

    @pytest.mark.asyncio
    async def test_retrieve_empty_user_sessions_from_repo(
        self,
        get_user_sessions_from_repo: GetUserSessionsFromRepoUseCase,
        mock_uow: AsyncMock,
    ) -> None:
        user_id = uuid4()
        mock_uow.user_sessions.get_user_sessions.return_value = []

        result = await get_user_sessions_from_repo(user_id)

        assert result == []
