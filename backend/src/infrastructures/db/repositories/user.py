from dataclasses import dataclass
from typing import final
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.user.repositories import UserRepositoryProtocol
from src.domain.entities.user import UserEntity
from src.infrastructures.db.exceptions import (
    RepositoryConflictError,
    RepositoryReadError,
    RepositorySaveError,
)
from src.infrastructures.db.mappers.user_db_mapper import UserDBMapper
from src.infrastructures.db.models.user import UserModel


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class UserRepositorySQLAlchemy(UserRepositoryProtocol):
    session: AsyncSession
    mapper: UserDBMapper

    async def get_by_email(self, email: str) -> UserEntity | None:
        try:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()

            return self.mapper.to_entity(user_model) if user_model else None

        except SQLAlchemyError as e:
            raise RepositoryReadError(
                f"Failed to retrieve user with email: '{email}' from database"
            ) from e

    async def get_by_id(self, user_id: UUID) -> UserEntity | None:
        try:
            stmt = select(UserModel).where(UserModel.user_id == user_id)
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()

            return self.mapper.to_entity(user_model) if user_model else None

        except SQLAlchemyError as e:
            raise RepositoryReadError(
                f"Failed to retrieve user with id: '{user_id}' from database"
            ) from e

    async def save(self, user: UserEntity) -> None:
        try:
            self.session.add(self.mapper.to_model(user))

        except IntegrityError as e:
            raise RepositoryConflictError(
                f"Conflict while saving user '{user.user_id}': {e}"
            ) from e

        except SQLAlchemyError as e:
            raise RepositorySaveError(f"Failed to save user '{user.user_id}': {e}") from e
