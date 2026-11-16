from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.application.dtos.token import AuthTokensDTO, TokenPayload


class TokenServiceProtocol(Protocol):
    @abstractmethod
    def decode_token(self, token: str) -> TokenPayload: ...

    @abstractmethod
    def create_token_pair(self, user_id: UUID, session_id: UUID) -> AuthTokensDTO: ...
