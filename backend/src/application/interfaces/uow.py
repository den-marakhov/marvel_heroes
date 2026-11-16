from abc import abstractmethod
from types import TracebackType
from typing import Protocol

from src.application.interfaces.hero.repositories import HeroRepositoryProtocol
from src.application.interfaces.user.repositories import UserRepositoryProtocol
from src.application.interfaces.user_session.repositories import (
    UserSessionRepositoryProtocol,
)


class UnitOfWorkProtocol(Protocol):
    heroes: HeroRepositoryProtocol
    users: UserRepositoryProtocol
    user_sessions: UserSessionRepositoryProtocol

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWorkProtocol": ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
