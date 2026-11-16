from dataclasses import dataclass
from typing import final
from uuid import UUID


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class LoginDTO:
    email: str
    password: str
    ip: str
    user_agent: str


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class CreateUserDTO:
    email: str
    name: str
    role: str
    password_hash: str


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UserDTO:
    user_id: UUID
    email: str
    name: str
    role: str
    password_hash: str
