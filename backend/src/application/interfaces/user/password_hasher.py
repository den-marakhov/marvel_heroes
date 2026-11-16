from abc import abstractmethod
from typing import Protocol


class PasswordHasherProtocol(Protocol):
    @abstractmethod
    async def hash(self, raw_password: str) -> str: ...

    @abstractmethod
    async def verify(self, raw_password: str, password_hash: str) -> bool: ...
