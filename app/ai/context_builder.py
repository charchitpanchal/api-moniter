from datetime import datetime
from sqlalchemy.orm import Session
from app.models.incident import Incident
from app.models.api_check import ApiCheck
from app.ai.schemas import IncidentContext

RECENT_ERRORS_LIMIT = 5  # keep prompts concise — see Day 21 cost-control rules


def build_incident_context(db: Session, incident: Incident) -> IncidentContext:
    """
    Gathers everything the AI needs from the database and packages it
    into a clean, structured IncidentContext. This is the ONLY place
    that reads raw DB models to build AI input — the AI module itself
    never touches SQLAlchemy models directly.
    """
    api = incident.api  # relationship already defined in Day 2's models

    recent_checks = (
        db.query(ApiCheck)
        .filter(ApiCheck.api_id == api.id, ApiCheck.success == False)  # noqa: E712
        .order_by(ApiCheck.checked_at.desc())
        .limit(RECENT_ERRORS_LIMIT)
        .all()
    )

    recent_errors = [
        check.error_message for check in recent_checks if check.error_message
    ]

    last_check = (
        db.query(ApiCheck)
        .filter(ApiCheck.api_id == api.id)
        .order_by(ApiCheck.checked_at.desc())
        .first()
    )

    end_time = incident.resolved_at or datetime.utcnow()
    duration_seconds = (end_time - incident.started_at).total_seconds()

    return IncidentContext(
        api_name=api.name,
        api_url=api.url,
        expected_status_code=api.expected_status_code,
        actual_status_code=last_check.status_code if last_check else None,
        response_time_ms=last_check.response_time if last_check else None,
        failure_count=incident.failure_count,
        recent_errors=recent_errors,
        incident_duration_seconds=round(duration_seconds, 2),
    )