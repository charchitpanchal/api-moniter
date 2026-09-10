import logging
from fastapi import HTTPException, status
from app.cache.client import redis_client

logger = logging.getLogger("redis.rate_limiter")


async def check_rate_limit(key: str, max_requests: int, window_seconds: int) -> None:
    """
    Sliding-window-ish fixed-window rate limiter using Redis INCR + EXPIRE.
    Raises HTTP 429 if the limit is exceeded. Fails OPEN (allows the request)
    if Redis itself is unavailable, so Redis being down never blocks the whole app.
    """
    try:
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, window_seconds)

        if current > max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {window_seconds} seconds.",
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"Rate limiter check failed (failing open): {e}")
        return  # Redis down -> don't block real traffic