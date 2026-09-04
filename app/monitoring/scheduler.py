import logging
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db.database import SessionLocal
from app.models.monitored_api import MonitoredApi
from app.models.api_check import ApiCheck
from app.services.monitoring_service import run_check_for_api

logger = logging.getLogger("monitoring.scheduler")

scheduler = AsyncIOScheduler()

TICK_INTERVAL_SECONDS = 10  # how often the scheduler wakes up to check "is anyone due?"


def _get_last_checked_at(db, api_id: int) -> datetime | None:
    last_check = (
        db.query(ApiCheck)
        .filter(ApiCheck.api_id == api_id)
        .order_by(ApiCheck.checked_at.desc())
        .first()
    )
    return last_check.checked_at if last_check else None


def _is_due(api: MonitoredApi, last_checked_at: datetime | None) -> bool:
    if last_checked_at is None:
        return True  # never checked before -> due immediately

    now = datetime.utcnow()
    elapsed = (now - last_checked_at).total_seconds()
    return elapsed >= api.monitoring_interval


async def run_due_checks():
    """
    Runs every TICK_INTERVAL_SECONDS. Looks at all active MonitoredApi
    records and runs a health check for any that are due based on
    their individual monitoring_interval.
    """
    db = SessionLocal()
    try:
        active_apis = db.query(MonitoredApi).filter(MonitoredApi.active == True).all()  # noqa: E712

        for api in active_apis:
            last_checked_at = _get_last_checked_at(db, api.id)

            if _is_due(api, last_checked_at):
                logger.info(f"Running scheduled check for API id={api.id} ({api.name})")
                try:
                    await run_check_for_api(db, api)
                except Exception as e:
                    # A single failing check must never take down the whole scheduler loop
                    logger.error(f"Scheduled check failed for API id={api.id}: {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        run_due_checks,
        trigger="interval",
        seconds=TICK_INTERVAL_SECONDS,
        id="monitoring_tick",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Monitoring scheduler started.")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Monitoring scheduler stopped.")