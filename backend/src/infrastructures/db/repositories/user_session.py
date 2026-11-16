from dataclasses import dataclass
from datetime import UTC, datetime
from typing import final
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.user_session.repositories import (
    UserSessionRepositoryProtocol,
)
from src.domain.entities.user_session import UserSessionEntity
from src.infrastructures.db.exceptions import (
    RepositoryConflictError,
    RepositoryReadError,
    RepositorySaveError,
)
from src.infrastructures.db.mappers.user_session_db_mapper import UserSessionDBMapper
from src.infrastructures.db.models.user_session import UserSessionModel


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class UserSessionRepositorySQLAlchemy(UserSessionRepositoryProtocol):
    session: AsyncSession
    mapper: UserSessionDBMapper

    async def get_user_session_by_id(
        self, session_id: UUID
    ) -> UserSessionEntity | None:
        try:
            stmt = select(UserSessionModel).where(
                UserSessionModel.session_id == session_id
            )
            result = await self.session.execute(stmt)
            user_session_model = result.scalar_one_or_none()

            return (
                self.mapper.to_entity(user_session_model)
                if user_session_model
                else None
            )

        except SQLAlchemyError as e:
            raise RepositoryReadError(
                f"Failed to retrieve user session with id: '{session_id}' "
                "from database"
            ) from e

    async def get_user_session_by_refresh_jti(
        self, refresh_jti: str
    ) -> UserSessionEntity | None:
        try:
            stmt = select(UserSessionModel).where(
                UserSessionModel.refresh_jti == refresh_jti
            )
            result = await self.session.execute(stmt)
            user_session_model = result.scalar_one_or_none()

            return (
                self.mapper.to_entity(user_session_model)
                if user_session_model
                else None
            )

        except SQLAlchemyError as e:
            raise RepositoryReadError(
                f"Failed to retrieve user session with refresh jti: '{refresh_jti}' "
                "from database"
            ) from e

    async def get_user_sessions(self, user_id: UUID) -> list[UserSessionEntity]:
        try:
            now = datetime.now(UTC)
            stmt = (
                select(UserSessionModel)
                .where(
                    UserSessionModel.user_id == user_id,
                    UserSessionModel.revoked_at.is_(None),
                    UserSessionModel.expires_at > now,
                )
                .order_by(UserSessionModel.last_seen_at.desc())
            )
            result = await self.session.execute(stmt)
            user_session_models = result.scalars().all()

            return [
                self.mapper.to_entity(user_session_model)
                for user_session_model in user_session_models
            ]

        except SQLAlchemyError as e:
            raise RepositoryReadError(
                f"Failed to retrieve user sessions for user '{user_id}' from database"
            ) from e

    async def get_all_user_sessions(self) -> list[UserSessionEntity]:
        try:
            now = datetime.now(UTC)
            stmt = (
                select(UserSessionModel)
                .where(
                    UserSessionModel.revoked_at.is_(None),
                    UserSessionModel.expires_at > now,
                )
                .order_by(UserSessionModel.last_seen_at.desc())
            )
            result = await self.session.execute(stmt)
            user_session_models = result.scalars().all()

            return [
                self.mapper.to_entity(user_session_model)
                for user_session_model in user_session_models
            ]

        except SQLAlchemyError as e:
            raise RepositoryReadError(
                "Failed to retrieve user sessions from database"
            ) from e

    async def save_user_session(
        self, user_session_entity: UserSessionEntity
    ) -> None:
        try:
            self.session.add(self.mapper.to_model(user_session_entity))

        except IntegrityError as e:
            raise RepositoryConflictError(
                f"Conflict while saving user session "
                f"'{user_session_entity.session_id}': {e}"
            ) from e

        except SQLAlchemyError as e:
            raise RepositorySaveError(
                f"Failed to save user session '{user_session_entity.session_id}': {e}"
            ) from e

    async def update_user_session(
        self, user_session_entity: UserSessionEntity
    ) -> None:
        try:
            stmt = select(UserSessionModel).where(
                UserSessionModel.session_id == user_session_entity.session_id
            )
            result = await self.session.execute(stmt)
            user_session_model = result.scalar_one_or_none()

            if user_session_model:
                self.mapper.update_model_from_entity(
                    user_session_model, user_session_entity
                )

        except IntegrityError as e:
            raise RepositoryConflictError(
                f"Conflict while saving user session "
                f"'{user_session_entity.session_id}': {e}"
            ) from e

        except SQLAlchemyError as e:
            raise RepositorySaveError(
                f"Failed to save user session '{user_session_entity.session_id}': {e}"
            ) from e

    async def revoke_session(self, session_id: UUID) -> None:
        try:
            stmt = (
                update(UserSessionModel)
                .where(
                    UserSessionModel.session_id == session_id,
                    UserSessionModel.revoked_at.is_(None),
                )
                .values(revoked_at=datetime.now(UTC))
            )
            await self.session.execute(stmt)

        except SQLAlchemyError as e:
            raise RepositorySaveError(
                f"Failed to revoke user session '{session_id}': {e}"
            ) from e

    async def revoke_all_user_sessions(self, user_id: UUID) -> None:
        try:
            stmt = (
                update(UserSessionModel)
                .where(
                    UserSessionModel.user_id == user_id,
                    UserSessionModel.revoked_at.is_(None),
                )
                .values(revoked_at=datetime.now(UTC))
            )
            await self.session.execute(stmt)

        except SQLAlchemyError as e:
            raise RepositorySaveError(
                f"Failed to revoke user sessions for user '{user_id}': {e}"
            ) from e
