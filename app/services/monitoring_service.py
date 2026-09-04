from sqlalchemy.orm import Session
from app.models.monitored_api import MonitoredApi
from app.monitoring.checker import perform_health_check
from app.repositories import check_repository


async def run_check_for_api(db: Session, api: MonitoredApi):
    """
    Runs a real health check against the given monitored API and
    persists the result. Returns the saved ApiCheck record.
    """
    result = await perform_health_check(api)
    check = check_repository.create_check(db, api.id, result)
    return check