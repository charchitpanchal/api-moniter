from sqlalchemy.orm import Session
from app.models.api_check import ApiCheck


def create_check(db: Session, api_id: int, result) -> ApiCheck:
    check = ApiCheck(
        api_id=api_id,
        status_code=result.status_code,
        response_time=result.response_time,
        success=result.success,
        error_message=result.error_message,
        timeout=result.timeout,
    )
    db.add(check)
    db.commit()
    db.refresh(check)
    return check


def list_checks_for_api(db: Session, api_id: int, limit: int = 50) -> list[ApiCheck]:
    return (
        db.query(ApiCheck)
        .filter(ApiCheck.api_id == api_id)
        .order_by(ApiCheck.checked_at.desc())
        .limit(limit)
        .all()
    )

def list_recent_checks_for_api(db, api_id: int, limit: int = 100) -> list[ApiCheck]:
    return (
        db.query(ApiCheck)
        .filter(ApiCheck.api_id == api_id)
        .order_by(ApiCheck.checked_at.desc())
        .limit(limit)
        .all()
    )