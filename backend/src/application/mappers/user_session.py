from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import final
from uuid import UUID

from src.application.dtos.token import TokenPayload, UpdateUserSessionTokensDTO
from src.application.dtos.user import LoginDTO
from src.application.dtos.user_session import CreateUserSessionDTO, UserSessionDTO
from src.application.interfaces.user_session.mappers import (
    UserSessionDtoEntityMapperProtocol,
)
from src.domain.entities.user_session import UserSessionEntity


@final
@dataclass(frozen=True, slots=True)
class UserSessionDtoEntityMapper(UserSessionDtoEntityMapperProtocol):
    def to_create_dto(
        self,
        dto: LoginDTO,
        *,
        session_id: UUID,
        user_id: UUID,
        access_payload: TokenPayload,
        refresh_payload: TokenPayload,
    ) -> CreateUserSessionDTO:
        return CreateUserSessionDTO(
            session_id=session_id,
            user_id=user_id,
            access_jti=access_payload.jti,
            refresh_jti=refresh_payload.jti,
            ip=dto.ip,
            user_agent=dto.user_agent,
            expires_at=datetime.now(UTC)
            + timedelta(seconds=refresh_payload.expires_in),
        )

    def to_entity_from_create_dto(
        self, dto: CreateUserSessionDTO
    ) -> UserSessionEntity:
        return UserSessionEntity(
            session_id=dto.session_id,
            user_id=dto.user_id,
            access_jti=dto.access_jti,
            refresh_jti=dto.refresh_jti,
            ip=dto.ip,
            user_agent=dto.user_agent,
            expires_at=dto.expires_at,
        )

    def to_dto(self, entity: UserSessionEntity) -> UserSessionDTO:
        return UserSessionDTO(
            session_id=entity.session_id,
            user_id=entity.user_id,
            ip=entity.ip,
            user_agent=entity.user_agent,
            location=entity.location,
            created_at=entity.created_at,
            last_seen_at=entity.last_seen_at,
            expires_at=entity.expires_at,
        )

    def to_dto_list(
        self, entities: list[UserSessionEntity]
    ) -> list[UserSessionDTO]:
        return [self.to_dto(entity) for entity in entities]

    def to_update_tokens_dto(
        self,
        user_session_entity: UserSessionEntity,
        *,
        access_ttl: int,
        refresh_ttl: int,
    ) -> UpdateUserSessionTokensDTO:
        return UpdateUserSessionTokensDTO(
            session_id=user_session_entity.session_id,
            user_id=user_session_entity.user_id,
            access_jti=user_session_entity.access_jti,
            refresh_jti=user_session_entity.refresh_jti,
            access_ttl=access_ttl,
            refresh_ttl=refresh_ttl,
        )
