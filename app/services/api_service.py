from sqlalchemy.orm import Session
from app.models.monitored_api import MonitoredApi
from app.models.user import User
from app.repositories import api_repository
from app.exceptions.custom import NotFoundException, ForbiddenException
from app.schemas.monitored_api import MonitoredApiCreate, MonitoredApiUpdate


def _to_db_dict(payload: MonitoredApiCreate | MonitoredApiUpdate) -> dict:
    """Convert Pydantic model to a plain dict, casting HttpUrl to str, dropping unset fields."""
    data = payload.model_dump(exclude_unset=True)
    if "url" in data and data["url"] is not None:
        data["url"] = str(data["url"])
    return data


def create_monitored_api(db: Session, user: User, payload: MonitoredApiCreate) -> MonitoredApi:
    data = _to_db_dict(payload)
    return api_repository.create_api(db, user.id, data)


def get_owned_api_or_404(db: Session, user: User, api_id: int) -> MonitoredApi:
    api = api_repository.get_api_by_id(db, api_id)
    if api is None:
        raise NotFoundException(detail="Monitored API not found")
    if api.user_id != user.id:
        raise ForbiddenException(detail="You do not own this monitored API")
    return api


def list_monitored_apis(db: Session, user: User) -> list[MonitoredApi]:
    return api_repository.list_apis_for_user(db, user.id)


def update_monitored_api(
    db: Session, user: User, api_id: int, payload: MonitoredApiUpdate
) -> MonitoredApi:
    api = get_owned_api_or_404(db, user, api_id)
    data = _to_db_dict(payload)
    return api_repository.update_api(db, api, data)


def delete_monitored_api(db: Session, user: User, api_id: int) -> None:
    api = get_owned_api_or_404(db, user, api_id)
    api_repository.delete_api(db, api)


def set_monitoring_active(db: Session, user: User, api_id: int, active: bool) -> MonitoredApi:
    api = get_owned_api_or_404(db, user, api_id)
    return api_repository.update_api(db, api, {"active": active})