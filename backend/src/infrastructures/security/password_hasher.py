import asyncio
from dataclasses import dataclass
from typing import final

from pwdlib import PasswordHash

from src.application.interfaces.user.password_hasher import PasswordHasherProtocol


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class Argon2PasswordHasher(PasswordHasherProtocol):
    hasher: PasswordHash

    def _hash(self, raw_password: str) -> str:
        return self.hasher.hash(raw_password)

    def _verify(self, raw_password: str, password_hash: str) -> bool:
        return self.hasher.verify(raw_password, password_hash)

    async def hash(self, raw_password: str) -> str:
        return await asyncio.to_thread(self._hash, raw_password)

    async def verify(self, raw_password: str, password_hash: str) -> bool:
        return await asyncio.to_thread(self._verify, raw_password, password_hash)
