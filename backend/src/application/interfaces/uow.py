from abc import abstractmethod
from typing import Protocol
from types import TracebackType

from src.application.interfaces.repositories import HeroRepositoryProtocol


class UnitOfWorkProtocol(Protocol):

	repository: HeroRepositoryProtocol

	@abstractmethod
	async def __aenter__(self) -> "UnitOfWorkProtocol":
		...

	@abstractmethod
	async def __aexit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None
		) -> None:
		...

	@abstractmethod
	async def commit(self) -> None:
		...

	@abstractmethod
	async def rollback(self) -> None:
		...