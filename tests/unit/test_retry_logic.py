import pytest
from unittest.mock import AsyncMock, patch
from app.monitoring.checker import CheckResult
from app.monitoring.retry import check_with_retries
from app.models.monitored_api import MonitoredApi


def make_fake_api():
    api = MonitoredApi(
        id=1, user_id=1, name="Test", url="https://example.com",
        method="GET", expected_status_code=200,
        monitoring_interval=60, timeout=5, active=True,
    )
    return api


@pytest.mark.asyncio
async def test_retry_succeeds_on_first_attempt():
    api = make_fake_api()
    success_result = CheckResult(status_code=200, response_time=100.0, success=True, error_message=None, timeout=False)

    with patch("app.monitoring.retry.perform_health_check", new=AsyncMock(return_value=success_result)):
        result, attempts = await check_with_retries(api)

    assert result.success is True
    assert attempts == 1


@pytest.mark.asyncio
async def test_retry_succeeds_after_transient_failure():
    api = make_fake_api()
    fail_result = CheckResult(status_code=500, response_time=100.0, success=False, error_message="fail", timeout=False)
    success_result = CheckResult(status_code=200, response_time=100.0, success=True, error_message=None, timeout=False)

    with patch(
        "app.monitoring.retry.perform_health_check",
        new=AsyncMock(side_effect=[fail_result, success_result]),
    ):
        result, attempts = await check_with_retries(api)

    assert result.success is True
    assert attempts == 2


@pytest.mark.asyncio
async def test_retry_exhausts_all_attempts_on_persistent_failure():
    api = make_fake_api()
    fail_result = CheckResult(status_code=500, response_time=100.0, success=False, error_message="fail", timeout=False)

    with patch("app.monitoring.retry.perform_health_check", new=AsyncMock(return_value=fail_result)):
        result, attempts = await check_with_retries(api)

    assert result.success is False
    assert attempts == 3  # matches DEFAULT_MAX_RETRIES