import asyncio
import os
from typing import List
from uuid import uuid4

from redis.asyncio import Redis

from app.core import reservations

TEST_REDIS_URL = os.getenv("TEST_REDIS_URL", "redis://localhost:6379/15")


def test_concurrent_slice_reservations_limited_to_available_inventory() -> None:
    async def run_test() -> None:
        redis = Redis.from_url(TEST_REDIS_URL, encoding="utf-8", decode_responses=True)
        try:
            await redis.flushdb()

            store_id = f"store-{uuid4()}"
            batch_id = f"batch-{uuid4()}"
            slice_ids: List[str] = [f"slice-{i}" for i in range(8)]

            await reservations.seed_available_slices(
                redis,
                store_id=store_id,
                batch_id=batch_id,
                slice_ids=slice_ids,
            )

            async def try_reserve(order_idx: int) -> str | None:
                return await reservations.reserve_next_available_slice(
                    redis,
                    store_id=store_id,
                    batch_id=batch_id,
                    order_reference=f"order-{order_idx}",
                    ttl_seconds=5,
                )

            results = await asyncio.gather(*[try_reserve(i) for i in range(20)])
            successes = [result for result in results if result is not None]

            assert len(successes) == 8
            assert len(successes) == len(set(successes))

            first_reserved = successes[0]
            ttl = await reservations.get_lock_ttl(redis, store_id=store_id, slice_id=first_reserved)
            assert ttl > 0

            remaining = await reservations.count_available_slices(redis, store_id=store_id, batch_id=batch_id)
            assert remaining == 0
        finally:
            await redis.flushdb()
            await redis.close()
            await redis.connection_pool.disconnect()

    asyncio.run(run_test())
