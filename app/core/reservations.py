from __future__ import annotations

from collections.abc import Iterable
from typing import Optional

from redis.asyncio import Redis

from app.core.settings import settings

_PREFIX = "mpf:stores"


def _available_key(store_id: str, batch_id: str) -> str:
    return f"{_PREFIX}:{store_id}:batches:{batch_id}:available"


def _lock_key(store_id: str, slice_id: str) -> str:
    return f"{_PREFIX}:{store_id}:slices:{slice_id}:lock"


async def seed_available_slices(
    redis: Redis,
    *,
    store_id: str,
    batch_id: str,
    slice_ids: Iterable[str],
) -> int:
    if not slice_ids:
        return 0
    return await redis.sadd(_available_key(store_id, batch_id), *[str(slice_id) for slice_id in slice_ids])


async def reserve_next_available_slice(
    redis: Redis,
    *,
    store_id: str,
    batch_id: str,
    order_reference: str,
    ttl_seconds: Optional[int] = None,
) -> Optional[str]:
    ttl = ttl_seconds or settings.REDIS_LOCK_TTL_SECONDS
    key = _available_key(store_id, batch_id)
    attempted: set[str] = set()

    while True:
        candidate = await redis.spop(key)
        if candidate is None:
            return None

        candidate = str(candidate)
        lock_key = _lock_key(store_id, candidate)

        locked = await redis.set(lock_key, order_reference, ex=ttl, nx=True)
        if locked:
            return candidate

        # Lock already exists, put slice back for another attempt.
        await redis.sadd(key, candidate)

        if candidate in attempted:
            # All available slices are locked at the moment.
            return None
        attempted.add(candidate)


async def release_slice(
    redis: Redis,
    *,
    store_id: str,
    batch_id: str,
    slice_id: str,
    requeue: bool = True,
) -> None:
    lock_key = _lock_key(store_id, slice_id)
    await redis.delete(lock_key)
    if requeue:
        await redis.sadd(_available_key(store_id, batch_id), slice_id)


async def count_available_slices(redis: Redis, *, store_id: str, batch_id: str) -> int:
    return await redis.scard(_available_key(store_id, batch_id))


async def get_lock_ttl(redis: Redis, *, store_id: str, slice_id: str) -> int:
    return await redis.ttl(_lock_key(store_id, slice_id))
