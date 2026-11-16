from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import final
from uuid import UUID

from src.domain.exceptions import DomainValidationError
from src.domain.value_objects.email import Email
from src.domain.value_objects.role import Role
from src.domain.value_objects.user_name import UserName


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UserEntity:
    user_id: UUID
    email: Email
    name: UserName
    password_hash: str
    role: Role
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.password_hash:
            raise DomainValidationError("Password hash must not be empty")
