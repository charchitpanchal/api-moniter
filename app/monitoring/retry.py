import asyncio
import logging
from app.models.monitored_api import MonitoredApi
from app.monitoring.checker import perform_health_check, CheckResult
from app.core.config import settings

logger = logging.getLogger("monitoring.retry")


async def check_with_retries(api: MonitoredApi) -> tuple[CheckResult, int]:
    """
    Performs a health check with retries on failure.
    Returns the FINAL result (last attempt) and the number of attempts made.
    If any attempt succeeds, returns immediately with that success.
    """
    attempts = 0
    result: CheckResult | None = None

    for attempt in range(1, settings.default_max_retries + 1):
        attempts = attempt
        result = await perform_health_check(api)

        if result.success:
            if attempt > 1:
                logger.info(f"API id={api.id} recovered on retry attempt {attempt}")
            return result, attempts

        if attempt < settings.default_max_retries:
            logger.warning(
                f"API id={api.id} check failed (attempt {attempt}/{settings.default_max_retries}), "
                f"retrying in {settings.default_retry_delay_seconds}s..."
            )
            await asyncio.sleep(settings.default_retry_delay_seconds)

    # All attempts exhausted, result is the last (failed) attempt
    return result, attempts