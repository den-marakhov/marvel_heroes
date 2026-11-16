from dataclasses import dataclass
from typing import final

from src.domain.exceptions import InvalidEmailException


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        normalized_value = self.value.strip().lower()
        object.__setattr__(self, "value", normalized_value)

        if len(normalized_value) < 6 or len(normalized_value) > 254:
            raise InvalidEmailException("Email must be between 6 and 254 characters")

        if normalized_value.count("@") != 1:
            raise InvalidEmailException(f"Invalid email: {normalized_value}")

        local, domain = normalized_value.split("@")
        if not local or not domain or "." not in domain:
            raise InvalidEmailException(f"Invalid email: {normalized_value}")

    def __str__(self):
        return self.value
