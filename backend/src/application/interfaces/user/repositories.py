from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.entities.user import UserEntity


class UserRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserEntity | None: ...

    @abstractmethod
    async def save(self, user: UserEntity) -> None: ...
