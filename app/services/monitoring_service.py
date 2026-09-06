from sqlalchemy.orm import Session
from app.models.monitored_api import MonitoredApi
from app.monitoring.retry import check_with_retries
from app.repositories import check_repository
from app.services import incident_service


async def run_check_for_api(db: Session, api: MonitoredApi):
    """
    Runs a health check WITH retries against the given monitored API,
    persists the final result, and manages the incident lifecycle
    (create/update/resolve) based on the outcome.
    """
    result, attempts = await check_with_retries(api)

    check = check_repository.create_check(db, api.id, result)

    if result.success:
        incident_service.handle_successful_check(db, api)
    else:
        incident_service.handle_failed_check(db, api, result.error_message, result.response_time)

    return check