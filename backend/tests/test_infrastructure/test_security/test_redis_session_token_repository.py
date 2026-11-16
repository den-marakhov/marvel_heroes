from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import redis.exceptions

from src.application.dtos.token import (
    AuthTokensDTO,
    TokenPayload,
    UpdateUserSessionTokensDTO,
)
from src.infrastructures.security.exceptions import TokenStorageError
from src.infrastructures.security.mappers.jwt_token_mapper import JwtTokenMapper
from src.infrastructures.security.redis_session_token_repository import (
    RedisSessionTokenRepository,
)


@pytest.fixture
def redis_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def session_token_repository(
    redis_client: AsyncMock,
) -> RedisSessionTokenRepository:
    return RedisSessionTokenRepository(client=redis_client, mapper=JwtTokenMapper())


def _tokens(*, user_id, session_id) -> AuthTokensDTO:
    return AuthTokensDTO(
        access_token="access-jwt",
        refresh_token="refresh-jwt",
        access_payload=_payload(
            user_id=user_id,
            session_id=session_id,
            jti="access-jti",
            token_type="access",
            expires_in=900,
        ),
        refresh_payload=_payload(
            user_id=user_id,
            session_id=session_id,
            jti="refresh-jti",
            token_type="refresh",
            expires_in=2_592_000,
        ),
    )


def _payload(*, user_id, session_id, jti: str, token_type: str, expires_in: int):
    return TokenPayload(
        user_id=user_id,
        session_id=session_id,
        jti=jti,
        token_type=token_type,  # type: ignore[arg-type]
        expires_in=expires_in,
    )


@pytest.mark.asyncio
async def test_save_token_pair(
    session_token_repository: RedisSessionTokenRepository,
    redis_client: AsyncMock,
) -> None:
    user_id = uuid4()
    session_id = uuid4()

    await session_token_repository.save_token_pair(
        _tokens(user_id=user_id, session_id=session_id)
    )

    redis_client.setex.assert_any_await(
        f"auth:session:{session_id}:access",
        900,
        "access-jti",
    )
    redis_client.setex.assert_any_await(
        f"auth:session:{session_id}:refresh",
        2_592_000,
        "refresh-jti",
    )
    redis_client.sadd.assert_awaited_once_with(
        f"auth:user:{user_id}:sessions",
        str(session_id),
    )


@pytest.mark.asyncio
async def test_update_session_tokens(
    session_token_repository: RedisSessionTokenRepository,
    redis_client: AsyncMock,
) -> None:
    user_id = uuid4()
    session_id = uuid4()

    await session_token_repository.update_session_tokens(
        UpdateUserSessionTokensDTO(
            session_id=session_id,
            user_id=user_id,
            access_jti="access-jti",
            refresh_jti="refresh-jti",
            access_ttl=400,
            refresh_ttl=2_592_000,
        )
    )

    redis_client.setex.assert_any_await(
        f"auth:session:{session_id}:access",
        400,
        "access-jti",
    )
    redis_client.setex.assert_any_await(
        f"auth:session:{session_id}:refresh",
        2_592_000,
        "refresh-jti",
    )
    redis_client.sadd.assert_awaited_once_with(
        f"auth:user:{user_id}:sessions",
        str(session_id),
    )


@pytest.mark.asyncio
async def test_get_access_token_jti(
    session_token_repository: RedisSessionTokenRepository,
    redis_client: AsyncMock,
) -> None:
    session_id = uuid4()
    redis_client.get.return_value = "access-jti"

    assert (
        await session_token_repository.get_access_token_jti(session_id)
        == "access-jti"
    )
    redis_client.get.assert_awaited_once_with(f"auth:session:{session_id}:access")


@pytest.mark.asyncio
async def test_get_refresh_token_jti_when_missing(
    session_token_repository: RedisSessionTokenRepository,
    redis_client: AsyncMock,
) -> None:
    redis_client.get.return_value = None

    assert await session_token_repository.get_refresh_token_jti(uuid4()) is None


@pytest.mark.asyncio
async def test_delete_tokens(
    session_token_repository: RedisSessionTokenRepository,
    redis_client: AsyncMock,
) -> None:
    user_id = uuid4()
    session_id = uuid4()

    await session_token_repository.delete_tokens(session_id, user_id)

    redis_client.delete.assert_awaited_once_with(
        f"auth:session:{session_id}:access",
        f"auth:session:{session_id}:refresh",
    )
    redis_client.srem.assert_awaited_once_with(
        f"auth:user:{user_id}:sessions",
        str(session_id),
    )


@pytest.mark.asyncio
async def test_delete_all(
    session_token_repository: RedisSessionTokenRepository,
    redis_client: AsyncMock,
) -> None:
    user_id = uuid4()
    session_id = str(uuid4())
    redis_client.smembers.return_value = {session_id}

    await session_token_repository.delete_all(user_id)

    redis_client.delete.assert_awaited_once_with(
        f"auth:session:{session_id}:access",
        f"auth:session:{session_id}:refresh",
        f"auth:user:{user_id}:sessions",
    )


@pytest.mark.asyncio
async def test_get_jti_fail_closed(
    session_token_repository: RedisSessionTokenRepository,
    redis_client: AsyncMock,
) -> None:
    redis_client.get.side_effect = redis.exceptions.RedisError("down")

    with pytest.raises(TokenStorageError):
        await session_token_repository.get_refresh_token_jti(uuid4())
