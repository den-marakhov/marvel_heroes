from dataclasses import dataclass
from typing import final

from src.domain.exceptions import InvalidPasswordException


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class RawPassword:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) < 8 or len(self.value) > 128:
            raise InvalidPasswordException(
                "Password must be between 8 and 128 characters"
            )

    def __str__(self):
        return self.value
