from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.api_check import ApiCheck
from app.schemas.metrics import ApiMetrics, ApiStatus
from app.models.monitored_api import MonitoredApi


def calculate_metrics(db: Session, api_id: int) -> ApiMetrics:
    checks = db.query(ApiCheck).filter(ApiCheck.api_id == api_id).all()

    total = len(checks)
    if total == 0:
        return ApiMetrics(
            api_id=api_id,
            total_checks=0,
            successful_checks=0,
            failed_checks=0,
            uptime_percentage=0.0,
            error_rate=0.0,
            average_response_time=None,
            min_response_time=None,
            max_response_time=None,
        )

    successful = sum(1 for c in checks if c.success)
    failed = total - successful

    response_times = [c.response_time for c in checks if c.response_time is not None]
    avg_rt = round(sum(response_times) / len(response_times), 2) if response_times else None
    min_rt = round(min(response_times), 2) if response_times else None
    max_rt = round(max(response_times), 2) if response_times else None

    uptime_pct = round((successful / total) * 100, 2)
    error_rate = round((failed / total) * 100, 2)

    return ApiMetrics(
        api_id=api_id,
        total_checks=total,
        successful_checks=successful,
        failed_checks=failed,
        uptime_percentage=uptime_pct,
        error_rate=error_rate,
        average_response_time=avg_rt,
        min_response_time=min_rt,
        max_response_time=max_rt,
    )


def get_current_status(db: Session, api: MonitoredApi) -> ApiStatus:
    last_check = (
        db.query(ApiCheck)
        .filter(ApiCheck.api_id == api.id)
        .order_by(ApiCheck.checked_at.desc())
        .first()
    )

    if last_check is None:
        current_status = "UNKNOWN"
    elif last_check.success:
        current_status = "HEALTHY"
    else:
        current_status = "DOWN"

    return ApiStatus(
        api_id=api.id,
        active=api.active,
        last_check_success=last_check.success if last_check else None,
        last_checked_at=last_check.checked_at.isoformat() if last_check else None,
        current_status=current_status,
    )