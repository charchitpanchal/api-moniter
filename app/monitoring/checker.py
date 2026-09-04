import time
import httpx
from dataclasses import dataclass
from app.models.monitored_api import MonitoredApi


@dataclass
class CheckResult:
    status_code: int | None
    response_time: float | None  # milliseconds
    success: bool
    error_message: str | None
    timeout: bool


async def perform_health_check(api: MonitoredApi) -> CheckResult:
    """
    Sends a real HTTP request to the monitored API's URL and returns
    a structured result. Never raises — all failure modes are captured
    and returned as a CheckResult so the caller can always save a record.
    """
    start = time.perf_counter()

    try:
        async with httpx.AsyncClient(timeout=api.timeout) as client:
            response = await client.request(
                method=api.method,
                url=api.url,
                headers=api.headers or None,
                json=api.request_body or None,
            )

        elapsed_ms = (time.perf_counter() - start) * 1000
        success = response.status_code == api.expected_status_code

        error_message = None
        if not success:
            error_message = (
                f"Expected status {api.expected_status_code}, "
                f"got {response.status_code}"
            )

        return CheckResult(
            status_code=response.status_code,
            response_time=round(elapsed_ms, 2),
            success=success,
            error_message=error_message,
            timeout=False,
        )

    except httpx.TimeoutException:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return CheckResult(
            status_code=None,
            response_time=round(elapsed_ms, 2),
            success=False,
            error_message=f"Request timed out after {api.timeout}s",
            timeout=True,
        )

    except httpx.ConnectError as e:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return CheckResult(
            status_code=None,
            response_time=round(elapsed_ms, 2),
            success=False,
            error_message=f"Connection error: {str(e)}",
            timeout=False,
        )

    except httpx.RequestError as e:
        # Covers DNS failures, invalid URLs, and other transport-level errors
        elapsed_ms = (time.perf_counter() - start) * 1000
        return CheckResult(
            status_code=None,
            response_time=round(elapsed_ms, 2),
            success=False,
            error_message=f"Request error: {str(e)}",
            timeout=False,
        )

    except Exception as e:
        # Last-resort catch-all so monitoring NEVER crashes the app
        elapsed_ms = (time.perf_counter() - start) * 1000
        return CheckResult(
            status_code=None,
            response_time=round(elapsed_ms, 2),
            success=False,
            error_message=f"Unexpected error: {str(e)}",
            timeout=False,
        )