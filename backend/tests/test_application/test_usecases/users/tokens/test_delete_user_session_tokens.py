from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.usecases.users.tokens.delete_user_session_tokens import (
    DeleteUserSessionTokensUseCase,
)


class TestDeleteUserSessionTokensUseCase:
    @pytest.fixture
    def mock_session_token_repository(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def delete_user_session_tokens(
        self, mock_session_token_repository: AsyncMock
    ) -> DeleteUserSessionTokensUseCase:
        return DeleteUserSessionTokensUseCase(
            session_token_repository=mock_session_token_repository,
        )

    @pytest.mark.asyncio
    async def test_deletes_session_tokens(
        self,
        delete_user_session_tokens: DeleteUserSessionTokensUseCase,
        mock_session_token_repository: AsyncMock,
    ) -> None:
        session_id = uuid4()
        user_id = uuid4()

        await delete_user_session_tokens(session_id=session_id, user_id=user_id)

        mock_session_token_repository.delete_tokens.assert_awaited_once_with(
            session_id, user_id
        )
