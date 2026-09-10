from sqlalchemy.orm import Session
from app.models.incident import Incident, IncidentStatus


def get_open_incident_for_api(db: Session, api_id: int) -> Incident | None:
    return (
        db.query(Incident)
        .filter(
            Incident.api_id == api_id,
            Incident.status.in_([IncidentStatus.OPEN, IncidentStatus.INVESTIGATING]),
        )
        .first()
    )


def create_incident(db: Session, api_id: int, severity, last_error: str) -> Incident:
    incident = Incident(
        api_id=api_id,
        status=IncidentStatus.OPEN,
        severity=severity,
        failure_count=1,
        last_error=last_error,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def increment_incident(db: Session, incident: Incident, severity, last_error: str) -> Incident:
    incident.failure_count += 1
    incident.severity = severity
    incident.last_error = last_error
    db.commit()
    db.refresh(incident)
    return incident


def resolve_incident(db: Session, incident: Incident) -> Incident:
    from datetime import datetime

    incident.status = IncidentStatus.RESOLVED
    incident.resolved_at = datetime.utcnow()
    incident.resolution_time = (incident.resolved_at - incident.started_at).total_seconds()
    db.commit()
    db.refresh(incident)
    return incident


def get_incident_by_id(db: Session, incident_id: int) -> Incident | None:
    return db.query(Incident).filter(Incident.id == incident_id).first()


def list_incidents_for_user(db: Session, user_id: int) -> list[Incident]:
    from app.models.monitored_api import MonitoredApi

    return (
        db.query(Incident)
        .join(MonitoredApi, Incident.api_id == MonitoredApi.id)
        .filter(MonitoredApi.user_id == user_id)
        .order_by(Incident.created_at.desc())
        .all()
    )