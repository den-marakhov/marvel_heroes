from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.application.dtos.token import AuthTokensDTO, TokenPayload
from src.application.dtos.user_session import CreateUserSessionDTO
from src.application.usecases.users.sessions.save_user_session_to_repo import (
    SaveUserSessionToRepoUseCase,
)
from src.domain.entities.user_session import UserSessionEntity


def _create_dto() -> CreateUserSessionDTO:
    now = datetime.now(UTC)
    return CreateUserSessionDTO(
        session_id=uuid4(),
        user_id=uuid4(),
        access_jti="access-jti",
        refresh_jti="refresh-jti",
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        expires_at=now + timedelta(days=30),
    )


def _user_session(dto: CreateUserSessionDTO) -> UserSessionEntity:
    return UserSessionEntity(
        session_id=dto.session_id,
        user_id=dto.user_id,
        access_jti=dto.access_jti,
        refresh_jti=dto.refresh_jti,
        ip=dto.ip,
        user_agent=dto.user_agent,
        expires_at=dto.expires_at,
    )


class TestSaveUserSessionToRepoUseCase:
    @pytest.fixture
    def mock_uow(self) -> AsyncMock:
        uow = AsyncMock()
        uow.user_sessions = AsyncMock()
        return uow

    @pytest.fixture
    def mock_session_token_repository(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def mock_mapper(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def save_user_session_to_repo(
        self,
        mock_uow: AsyncMock,
        mock_session_token_repository: AsyncMock,
        mock_mapper: MagicMock,
    ) -> SaveUserSessionToRepoUseCase:
        return SaveUserSessionToRepoUseCase(
            uow=mock_uow,
            session_token_repository=mock_session_token_repository,
            mapper=mock_mapper,
        )

    @pytest.mark.asyncio
    async def test_saves_session_and_token_pair(
        self,
        save_user_session_to_repo: SaveUserSessionToRepoUseCase,
        mock_uow: AsyncMock,
        mock_session_token_repository: AsyncMock,
        mock_mapper: MagicMock,
    ) -> None:
        dto = _create_dto()
        tokens = AuthTokensDTO(
            access_token="access-jwt",
            refresh_token="refresh-jwt",
            access_payload=TokenPayload(
                user_id=dto.user_id,
                session_id=dto.session_id,
                jti="access-jti",
                token_type="access",
                expires_in=900,
            ),
            refresh_payload=TokenPayload(
                user_id=dto.user_id,
                session_id=dto.session_id,
                jti="refresh-jti",
                token_type="refresh",
                expires_in=2_592_000,
            ),
        )
        user_session_entity = _user_session(dto)
        mock_mapper.to_entity_from_create_dto.return_value = user_session_entity

        await save_user_session_to_repo(dto, tokens)

        mock_mapper.to_entity_from_create_dto.assert_called_once_with(dto)
        mock_uow.user_sessions.save_user_session.assert_awaited_once_with(
            user_session_entity
        )
        mock_session_token_repository.save_token_pair.assert_awaited_once_with(tokens)
