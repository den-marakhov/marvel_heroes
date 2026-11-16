from dataclasses import dataclass
from typing import Any, final
from uuid import UUID

from src.application.dtos.user import UserDTO
from src.application.interfaces.user.serialization import (
    UserSerializationMapperProtocol,
)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UserSerializationMapper(UserSerializationMapperProtocol):
    def to_dict(self, user_dto: UserDTO) -> dict[str, Any]:
        return {
            "user_id": str(user_dto.user_id),
            "email": user_dto.email,
            "name": user_dto.name,
            "role": user_dto.role,
            "password_hash": user_dto.password_hash,
        }

    def from_dict(self, data: dict[str, Any]) -> UserDTO:
        return UserDTO(
            user_id=UUID(data["user_id"]),
            email=data["email"],
            name=data["name"],
            role=data["role"],
            password_hash=data["password_hash"],
        )
