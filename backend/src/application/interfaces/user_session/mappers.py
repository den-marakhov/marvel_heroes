from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.application.dtos.token import TokenPayload, UpdateUserSessionTokensDTO
from src.application.dtos.user import LoginDTO
from src.application.dtos.user_session import CreateUserSessionDTO, UserSessionDTO
from src.domain.entities.user_session import UserSessionEntity


class UserSessionDtoEntityMapperProtocol(Protocol):
    @abstractmethod
    def to_create_dto(
        self,
        dto: LoginDTO,
        *,
        session_id: UUID,
        user_id: UUID,
        access_payload: TokenPayload,
        refresh_payload: TokenPayload,
    ) -> CreateUserSessionDTO: ...

    @abstractmethod
    def to_entity_from_create_dto(
        self, dto: CreateUserSessionDTO
    ) -> UserSessionEntity: ...

    @abstractmethod
    def to_dto(self, entity: UserSessionEntity) -> UserSessionDTO: ...

    @abstractmethod
    def to_dto_list(
        self, entities: list[UserSessionEntity]
    ) -> list[UserSessionDTO]: ...

    @abstractmethod
    def to_update_tokens_dto(
        self,
        user_session_entity: UserSessionEntity,
        *,
        access_ttl: int,
        refresh_ttl: int,
    ) -> UpdateUserSessionTokensDTO: ...
