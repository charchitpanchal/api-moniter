import json
import logging
from app.cache.client import redis_client

logger = logging.getLogger("redis.cache")

STATUS_CACHE_TTL = 10       # seconds
METRICS_CACHE_TTL = 15      # seconds


def _status_key(api_id: int) -> str:
    return f"status:{api_id}"


def _metrics_key(api_id: int) -> str:
    return f"metrics:{api_id}"


async def get_cached_status(api_id: int) -> dict | None:
    try:
        raw = await redis_client.get(_status_key(api_id))
        return json.loads(raw) if raw else None
    except Exception as e:
        logger.warning(f"Redis GET failed for status:{api_id}: {e}")
        return None  # fail gracefully -> caller falls back to DB


async def set_cached_status(api_id: int, data: dict) -> None:
    try:
        await redis_client.set(_status_key(api_id), json.dumps(data), ex=STATUS_CACHE_TTL)
    except Exception as e:
        logger.warning(f"Redis SET failed for status:{api_id}: {e}")


async def invalidate_status(api_id: int) -> None:
    try:
        await redis_client.delete(_status_key(api_id))
    except Exception as e:
        logger.warning(f"Redis DELETE failed for status:{api_id}: {e}")


async def get_cached_metrics(api_id: int) -> dict | None:
    try:
        raw = await redis_client.get(_metrics_key(api_id))
        return json.loads(raw) if raw else None
    except Exception as e:
        logger.warning(f"Redis GET failed for metrics:{api_id}: {e}")
        return None


async def set_cached_metrics(api_id: int, data: dict) -> None:
    try:
        await redis_client.set(_metrics_key(api_id), json.dumps(data), ex=METRICS_CACHE_TTL)
    except Exception as e:
        logger.warning(f"Redis SET failed for metrics:{api_id}: {e}")