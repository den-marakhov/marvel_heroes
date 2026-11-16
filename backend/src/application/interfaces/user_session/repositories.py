from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.entities.user_session import UserSessionEntity


class UserSessionRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_user_sessions(self, user_id: UUID) -> list[UserSessionEntity]: ...

    @abstractmethod
    async def get_all_user_sessions(self) -> list[UserSessionEntity]: ...

    @abstractmethod
    async def get_user_session_by_id(
        self, session_id: UUID
    ) -> UserSessionEntity | None: ...

    @abstractmethod
    async def get_user_session_by_refresh_jti(
        self, refresh_jti: str
    ) -> UserSessionEntity | None: ...

    @abstractmethod
    async def save_user_session(
        self, user_session_entity: UserSessionEntity
    ) -> None: ...

    @abstractmethod
    async def update_user_session(
        self, user_session_entity: UserSessionEntity
    ) -> None: ...

    @abstractmethod
    async def revoke_session(self, session_id: UUID) -> None: ...

    @abstractmethod
    async def revoke_all_user_sessions(self, user_id: UUID) -> None: ...
