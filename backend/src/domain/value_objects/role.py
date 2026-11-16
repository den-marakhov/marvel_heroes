from dataclasses import dataclass
from typing import final

from src.domain.constants import ALLOWED_ROLES
from src.domain.exceptions import InvalidRoleException


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class Role:
    value: str

    def __post_init__(self) -> None:
        if self.value not in ALLOWED_ROLES:
            raise InvalidRoleException(f"Invalid role: {self.value}")

    def __str__(self):
        return self.value
