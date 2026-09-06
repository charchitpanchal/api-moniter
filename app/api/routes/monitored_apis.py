from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.monitored_api import MonitoredApiCreate, MonitoredApiUpdate, MonitoredApiOut
from app.schemas.api_check import ApiCheckOut
from app.schemas.metrics import ApiMetrics, ApiStatus
from app.services import api_service, monitoring_service, metrics_service
from app.repositories import check_repository
from app.cache.rate_limiter import check_rate_limit

router = APIRouter(prefix="/api/monitored-apis", tags=["Monitored APIs"])


@router.post("", response_model=MonitoredApiOut, status_code=status.HTTP_201_CREATED)
async def create_monitored_api(
    payload: MonitoredApiCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await check_rate_limit(f"rate_limit:create_api:{current_user.id}", max_requests=10, window_seconds=60)
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


@router.post("/{api_id}/check-now", response_model=ApiCheckOut)
async def check_now(
    api_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Manually trigger a single health check against this API right now."""
    api = api_service.get_owned_api_or_404(db, current_user, api_id)
    return await monitoring_service.run_check_for_api(db, api)


@router.get("/{api_id}/checks", response_model=list[ApiCheckOut])
def get_checks(
    api_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """View recent check history for this API."""
    api_service.get_owned_api_or_404(db, current_user, api_id)
    return check_repository.list_checks_for_api(db, api_id, limit)


@router.get("/{api_id}/metrics", response_model=ApiMetrics)
async def get_metrics(
    api_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    api_service.get_owned_api_or_404(db, current_user, api_id)
    return await metrics_service.calculate_metrics(db, api_id)


@router.get("/{api_id}/status", response_model=ApiStatus)
async def get_status(
    api_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    api = api_service.get_owned_api_or_404(db, current_user, api_id)
    return await metrics_service.get_current_status(db, api)