from sqlalchemy.orm import Session
from app.models.monitored_api import MonitoredApi
from app.monitoring.retry import check_with_retries
from app.repositories import check_repository
from app.services import incident_service
from app.cache import cache


async def run_check_for_api(db: Session, api: MonitoredApi):
    result, attempts = await check_with_retries(api)

    check = check_repository.create_check(db, api.id, result)

    if result.success:
        await incident_service.handle_successful_check(db, api)
    else:
        await incident_service.handle_failed_check(db, api, result.error_message, result.response_time)

    await cache.invalidate_status(api.id)  # status just changed -> force fresh read next time

    return check