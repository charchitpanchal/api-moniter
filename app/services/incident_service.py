import logging
from sqlalchemy.orm import Session
from app.models.monitored_api import MonitoredApi
from app.models.incident import IncidentSeverity
from app.repositories import incident_repository

logger = logging.getLogger("services.incident")


def determine_severity(failure_count: int, response_time: float | None, api: MonitoredApi) -> IncidentSeverity:
    """
    Simple, explainable severity rules:
    - CRITICAL: many consecutive failures (sustained outage)
    - HIGH: several consecutive failures, or failures with very high latency
    - MEDIUM: repeated failures (more than 1)
    - LOW: first failure of a new incident
    """
    if failure_count >= 6:
        return IncidentSeverity.CRITICAL
    if failure_count >= 4:
        return IncidentSeverity.HIGH
    if failure_count >= 2:
        return IncidentSeverity.MEDIUM
    return IncidentSeverity.LOW


def handle_failed_check(db: Session, api: MonitoredApi, error_message: str, response_time: float | None):
    """
    Called when a check has failed after all retries.
    Creates a new incident, or updates the existing OPEN one (deduplication).
    """
    existing = incident_repository.get_open_incident_for_api(db, api.id)

    if existing is None:
        severity = determine_severity(1, response_time, api)
        incident = incident_repository.create_incident(db, api.id, severity, error_message)
        logger.warning(f"NEW incident #{incident.id} created for API id={api.id} ({api.name})")
        return incident
    else:
        new_failure_count = existing.failure_count + 1
        severity = determine_severity(new_failure_count, response_time, api)
        incident = incident_repository.increment_incident(db, existing, severity, error_message)
        logger.warning(
            f"Incident #{incident.id} updated for API id={api.id} "
            f"(failure_count={incident.failure_count}, severity={incident.severity})"
        )
        return incident


def handle_successful_check(db: Session, api: MonitoredApi):
    """
    Called when a check succeeds. If there's an open incident for this API,
    resolve it — the outage is over.
    """
    existing = incident_repository.get_open_incident_for_api(db, api.id)

    if existing is not None:
        incident = incident_repository.resolve_incident(db, existing)
        logger.info(
            f"Incident #{incident.id} RESOLVED for API id={api.id} "
            f"(duration={incident.resolution_time}s)"
        )
        return incident
    return None