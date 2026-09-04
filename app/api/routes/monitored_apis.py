from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.monitored_api import MonitoredApiCreate, MonitoredApiUpdate, MonitoredApiOut
from app.services import api_service

router = APIRouter(prefix="/api/monitored-apis", tags=["Monitored APIs"])


@router.post("", response_model=MonitoredApiOut, status_code=status.HTTP_201_CREATED)
def create_monitored_api(
    payload: MonitoredApiCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return api_service.create_monitored_api(db, current_user, payload)


@router.get("", response_model=list[MonitoredApiOut])
def list_monitored_apis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return api_service.list_monitored_apis(db, current_user)


@router.get("/{api_id}", response_model=MonitoredApiOut)
def get_monitored_api(
    api_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return api_service.get_owned_api_or_404(db, current_user, api_id)


@router.put("/{api_id}", response_model=MonitoredApiOut)
def update_monitored_api(
    api_id: int,
    payload: MonitoredApiUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return api_service.update_monitored_api(db, current_user, api_id, payload)


@router.delete("/{api_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_monitored_api(
    api_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    api_service.delete_monitored_api(db, current_user, api_id)


@router.patch("/{api_id}/enable", response_model=MonitoredApiOut)
def enable_monitoring(
    api_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return api_service.set_monitoring_active(db, current_user, api_id, True)


@router.patch("/{api_id}/disable", response_model=MonitoredApiOut)
def disable_monitoring(
    api_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return api_service.set_monitoring_active(db, current_user, api_id, False)