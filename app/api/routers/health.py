from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, status
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.redis import get_redis

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health(
    db: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> dict[str, Any]:
    errors: dict[str, str] = {}

    try:
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as exc:  # pylint: disable=broad-except
        db_status = "error"
        errors["database"] = str(exc)

    try:
        await redis.ping()
        redis_status = "ok"
    except Exception as exc:  # pylint: disable=broad-except
        redis_status = "error"
        errors["redis"] = str(exc)

    overall = "ok" if not errors else "degraded"

    return {
        "status": overall,
        "database": db_status,
        "redis": redis_status,
        "errors": errors,
    }
