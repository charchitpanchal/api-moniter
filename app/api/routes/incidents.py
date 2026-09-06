from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.incident import IncidentOut, IncidentUpdate
from app.schemas.ai_analysis import AiAnalysisOut
from app.repositories import incident_repository
from app.services import ai_analysis_service
from app.exceptions.custom import NotFoundException, ForbiddenException

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])


def _get_owned_incident_or_404(db: Session, current_user: User, incident_id: int):
    incident = incident_repository.get_incident_by_id(db, incident_id)
    if incident is None:
        raise NotFoundException(detail="Incident not found")
    if incident.api.user_id != current_user.id:
        raise ForbiddenException(detail="You do not own this incident")
    return incident


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
    return _get_owned_incident_or_404(db, current_user, incident_id)


@router.patch("/{incident_id}", response_model=IncidentOut)
def update_incident(
    incident_id: int,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = _get_owned_incident_or_404(db, current_user, incident_id)

    if payload.status is not None:
        incident.status = payload.status
        db.commit()
        db.refresh(incident)

    return incident


@router.post("/{incident_id}/analyze", response_model=AiAnalysisOut)
async def analyze_incident_endpoint(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Triggers AI root-cause analysis for this incident and stores the result."""
    incident = _get_owned_incident_or_404(db, current_user, incident_id)
    return await ai_analysis_service.run_analysis_for_incident(db, incident)


@router.get("/{incident_id}/analysis", response_model=AiAnalysisOut)
def get_analysis(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves the most recent AI analysis for this incident, if one exists."""
    _get_owned_incident_or_404(db, current_user, incident_id)  # ownership check
    return ai_analysis_service.get_latest_analysis_or_404(db, incident_id)