from sqlalchemy.orm import Session
from app.models.monitored_api import MonitoredApi


def create_api(db: Session, user_id: int, data: dict) -> MonitoredApi:
    api = MonitoredApi(user_id=user_id, **data)
    db.add(api)
    db.commit()
    db.refresh(api)
    return api


def get_api_by_id(db: Session, api_id: int) -> MonitoredApi | None:
    return db.query(MonitoredApi).filter(MonitoredApi.id == api_id).first()


def list_apis_for_user(db: Session, user_id: int) -> list[MonitoredApi]:
    return db.query(MonitoredApi).filter(MonitoredApi.user_id == user_id).all()


def update_api(db: Session, api: MonitoredApi, data: dict) -> MonitoredApi:
    for key, value in data.items():
        setattr(api, key, value)
    db.commit()
    db.refresh(api)
    return api


def delete_api(db: Session, api: MonitoredApi) -> None:
    db.delete(api)
    db.commit()