from dataclasses import dataclass
from typing import final

from src.domain.entities.user_session import UserSessionEntity
from src.infrastructures.db.models.user import UserModel  # noqa: F401
from src.infrastructures.db.models.user_session import UserSessionModel


@final
@dataclass(frozen=True, slots=True)
class UserSessionDBMapper:
    def to_model(self, entity: UserSessionEntity) -> UserSessionModel:
        return UserSessionModel(
            session_id=entity.session_id,
            user_id=entity.user_id,
            refresh_jti=entity.refresh_jti,
            access_jti=entity.access_jti,
            ip=entity.ip,
            user_agent=entity.user_agent,
            location=entity.location,
            expires_at=entity.expires_at,
            last_seen_at=entity.last_seen_at,
            revoked_at=entity.revoked_at,
            created_at=entity.created_at,
        )

    def to_entity(self, model: UserSessionModel) -> UserSessionEntity:
        return UserSessionEntity(
            session_id=model.session_id,
            user_id=model.user_id,
            refresh_jti=model.refresh_jti,
            access_jti=model.access_jti,
            ip=model.ip,
            user_agent=model.user_agent,
            location=model.location,
            expires_at=model.expires_at,
            last_seen_at=model.last_seen_at,
            revoked_at=model.revoked_at,
            created_at=model.created_at,
        )

    def update_model_from_entity(
        self, model: UserSessionModel, entity: UserSessionEntity
    ) -> None:
        model.refresh_jti = entity.refresh_jti
        model.access_jti = entity.access_jti
        model.ip = entity.ip
        model.user_agent = entity.user_agent
        model.location = entity.location
        model.expires_at = entity.expires_at
        model.last_seen_at = entity.last_seen_at
        model.revoked_at = entity.revoked_at
