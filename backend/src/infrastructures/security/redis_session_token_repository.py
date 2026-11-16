from dataclasses import dataclass
from typing import final
from uuid import UUID

from redis.asyncio import Redis
from redis.exceptions import RedisError
import structlog

from src.application.dtos.token import AuthTokensDTO, UpdateUserSessionTokensDTO
from src.application.interfaces.user.session_token_repository import (
    SessionTokenRepositoryProtocol,
)
from src.infrastructures.security.exceptions import TokenStorageError
from src.infrastructures.security.mappers.jwt_token_mapper import JwtTokenMapper

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class RedisSessionTokenRepository(SessionTokenRepositoryProtocol):
    client: Redis
    mapper: JwtTokenMapper

    async def save_token_pair(self, tokens: AuthTokensDTO) -> None:
        update_user_session_tokens_dto = self.mapper.to_update_session_tokens_dto(
            tokens
        )
        await self.update_session_tokens(update_user_session_tokens_dto)

    async def update_session_tokens(
        self, update_user_session_tokens_dto: UpdateUserSessionTokensDTO
    ) -> None:
        session_id = update_user_session_tokens_dto.session_id
        user_id = update_user_session_tokens_dto.user_id
        access_token_key = f"auth:session:{session_id}:access"
        refresh_token_key = f"auth:session:{session_id}:refresh"
        user_sessions_index_key = f"auth:user:{user_id}:sessions"
        try:
            await self.client.setex(
                access_token_key,
                max(update_user_session_tokens_dto.access_ttl, 1),
                update_user_session_tokens_dto.access_jti,
            )
            await self.client.setex(
                refresh_token_key,
                max(update_user_session_tokens_dto.refresh_ttl, 1),
                update_user_session_tokens_dto.refresh_jti,
            )
            await self.client.sadd(user_sessions_index_key, str(session_id))
        except RedisError as error:
            logger.error(
                "Redis update session tokens failed",
                session_id=session_id,
                error=str(error),
            )
            raise TokenStorageError(
                f"Failed to save tokens for session '{session_id}'"
            ) from error

    async def get_access_token_jti(self, session_id: UUID) -> str | None:
        access_token_key = f"auth:session:{session_id}:access"
        try:
            return await self.client.get(access_token_key)
        except RedisError as error:
            logger.error(
                "Redis get access token failed",
                session_id=session_id,
                error=str(error),
            )
            raise TokenStorageError(
                f"Failed to get access token for session '{session_id}'"
            ) from error

    async def get_refresh_token_jti(self, session_id: UUID) -> str | None:
        refresh_token_key = f"auth:session:{session_id}:refresh"
        try:
            return await self.client.get(refresh_token_key)
        except RedisError as error:
            logger.error(
                "Redis get refresh token failed",
                session_id=session_id,
                error=str(error),
            )
            raise TokenStorageError(
                f"Failed to get refresh token for session '{session_id}'"
            ) from error

    async def delete_tokens(self, session_id: UUID, user_id: UUID) -> None:
        access_token_key = f"auth:session:{session_id}:access"
        refresh_token_key = f"auth:session:{session_id}:refresh"
        user_sessions_index_key = f"auth:user:{user_id}:sessions"
        try:
            await self.client.delete(access_token_key, refresh_token_key)
            await self.client.srem(user_sessions_index_key, str(session_id))
        except RedisError as error:
            logger.error(
                "Redis delete session tokens failed",
                session_id=session_id,
                error=str(error),
            )
            raise TokenStorageError(
                f"Failed to delete tokens for session '{session_id}'"
            ) from error

    async def delete_all(self, user_id: UUID) -> None:
        user_sessions_index_key = f"auth:user:{user_id}:sessions"
        try:
            stored_session_ids = await self.client.smembers(
                user_sessions_index_key
            )
            redis_keys_to_delete = []
            for stored_session_id in stored_session_ids:
                redis_keys_to_delete.append(
                    f"auth:session:{stored_session_id}:access"
                )
                redis_keys_to_delete.append(
                    f"auth:session:{stored_session_id}:refresh"
                )
            redis_keys_to_delete.append(user_sessions_index_key)
            await self.client.delete(*redis_keys_to_delete)
        except RedisError as error:
            logger.error(
                "Redis delete all tokens failed",
                user_id=user_id,
                error=str(error),
            )
            raise TokenStorageError(
                f"Failed to delete tokens for user '{user_id}'"
            ) from error
