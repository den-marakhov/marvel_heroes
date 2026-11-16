from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.application.dtos.token import AuthTokensDTO, UpdateUserSessionTokensDTO


class SessionTokenRepositoryProtocol(Protocol):
    @abstractmethod
    async def save_token_pair(self, tokens: AuthTokensDTO) -> None: ...

    @abstractmethod
    async def update_session_tokens(
        self, update_user_session_tokens_dto: UpdateUserSessionTokensDTO
    ) -> None: ...

    @abstractmethod
    async def get_access_token_jti(self, session_id: UUID) -> str | None: ...

    @abstractmethod
    async def get_refresh_token_jti(self, session_id: UUID) -> str | None: ...

    @abstractmethod
    async def delete_tokens(self, session_id: UUID, user_id: UUID) -> None: ...

    @abstractmethod
    async def delete_all(self, user_id: UUID) -> None: ...
