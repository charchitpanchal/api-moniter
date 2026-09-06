from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.incident import IncidentOut, IncidentUpdate
from app.repositories import incident_repository
from app.exceptions.custom import NotFoundException, ForbiddenException

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])


@router.get("", response_model=list[IncidentOut])
def list_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return incident_repository.list_incidents_for_user(db, current_user.id)


@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = incident_repository.get_incident_by_id(db, incident_id)
    if incident is None:
        raise NotFoundException(detail="Incident not found")
    if incident.api.user_id != current_user.id:
        raise ForbiddenException(detail="You do not own this incident")
    return incident


@router.patch("/{incident_id}", response_model=IncidentOut)
def update_incident(
    incident_id: int,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = incident_repository.get_incident_by_id(db, incident_id)
    if incident is None:
        raise NotFoundException(detail="Incident not found")
    if incident.api.user_id != current_user.id:
        raise ForbiddenException(detail="You do not own this incident")

    if payload.status is not None:
        incident.status = payload.status
        db.commit()
        db.refresh(incident)

    return incident