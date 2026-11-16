from dataclasses import dataclass
from typing import final

from src.domain.exceptions import InvalidUserNameException


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UserName:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) < 2 or len(self.value) > 100:
            raise InvalidUserNameException(
                "User name must be between 2 and 100 characters"
            )

    def __str__(self):
        return self.value
