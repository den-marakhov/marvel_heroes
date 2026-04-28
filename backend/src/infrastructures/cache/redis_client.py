from dataclasses import dataclass
import json
from typing import Any, final

from redis.asyncio import Redis
import redis.exceptions
import structlog

from src.application.interfaces.cache import CacheProtocol

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class RedisCacheClient(CacheProtocol):
    client: Redis
    ttl: int | None = None

    async def get(self, key: str) -> dict[str, Any] | None:

        try:
            value = await self.client.get(key)
            if value is None:
                return None

            return json.loads(value)

        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error("Redis 'get' operation failed", key=key, error=str(e))
            return None

        except (json.JSONDecodeError, TypeError) as e:
            logger.warning("Decoding cache operation failed", key=key, error=str(e))
            return None

    async def set(
        self, key: str, value: dict[str, Any], ttl: int | None = None
    ) -> bool:

        try:
            serialized_value_from_json = json.dumps(value, default=str)

            if ttl is not None:
                await self.client.setex(key, ttl, serialized_value_from_json)
            elif self.ttl is not None:
                await self.client.setex(key, self.ttl, serialized_value_from_json)
            else:
                await self.client.set(key, serialized_value_from_json)
            return True

        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error("Redis 'set' operation failed", key=key, error=str(e))
            return False

        except (TypeError, ValueError) as e:
            logger.error(
                "Failed to serialize value from json fro cache", key=key, error=str(e)
            )
            return False

    async def delete(self, key: str) -> bool:

        try:
            result = await self.client.delete(key)
            return result > 0

        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error("Redis 'delete' operation failed", key=key, error=str(e))
            return False

    async def exists(self, key: str) -> bool:

        try:
            return bool(await self.client.exists(key))

        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error("Redis 'exists' operation failed", key=key, error=str(e))
            return False

    async def clear(self, pattern: str) -> int:
        try:
            keys = []
            async for key in self.client.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                deleted_keys_qnty = await self.client.delete(*keys)
                logger.info(
                    "Redis clear keys operation by pattern completed",
                    deleted_quantity=deleted_keys_qnty,
                )
                return deleted_keys_qnty

            return 0

        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error(
                "Redis 'clear' operation failed", pattern=pattern, error=str(e)
            )
            return 0

    async def close(self) -> None:
        try:
            await self.client.close()
            logger.info("Redis connection has been closed")

        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error("Failed to close Redis connection", error=str(e))
