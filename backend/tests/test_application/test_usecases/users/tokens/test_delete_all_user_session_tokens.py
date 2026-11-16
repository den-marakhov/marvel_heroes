from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.usecases.users.tokens.delete_all_user_session_tokens import (
    DeleteAllUserSessionTokensUseCase,
)


class TestDeleteAllUserSessionTokensUseCase:
    @pytest.fixture
    def mock_session_token_repository(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def delete_all_user_session_tokens(
        self, mock_session_token_repository: AsyncMock
    ) -> DeleteAllUserSessionTokensUseCase:
        return DeleteAllUserSessionTokensUseCase(
            session_token_repository=mock_session_token_repository,
        )

    @pytest.mark.asyncio
    async def test_deletes_all_session_tokens(
        self,
        delete_all_user_session_tokens: DeleteAllUserSessionTokensUseCase,
        mock_session_token_repository: AsyncMock,
    ) -> None:
        user_id = uuid4()

        await delete_all_user_session_tokens(user_id)

        mock_session_token_repository.delete_all.assert_awaited_once_with(user_id)
