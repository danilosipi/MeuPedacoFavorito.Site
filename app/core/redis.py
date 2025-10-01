from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Optional

from redis.asyncio import Redis

from app.core.settings import settings

_redis: Optional[Redis] = None


async def init_redis() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis


async def close_redis() -> None:
    global _redis
    if _redis is None:
        return
    try:
        await _redis.close()
    finally:
        await _redis.connection_pool.disconnect()  # type: ignore[union-attr]
        _redis = None


async def get_redis() -> AsyncIterator[Redis]:
    client = await init_redis()
    yield client
