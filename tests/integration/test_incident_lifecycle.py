from app.services import incident_service
from app.models.incident import IncidentStatus, IncidentSeverity
from app.models.monitored_api import MonitoredApi
from app.models.user import User
import pytest


@pytest.fixture
def test_api(db_session):
    user = User(name="Test", email="incidenttest@example.com", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    api = MonitoredApi(
        user_id=user.id, name="Test API", url="https://example.com",
        method="GET", expected_status_code=200,
        monitoring_interval=60, timeout=5, active=True,
    )
    db_session.add(api)
    db_session.commit()
    db_session.refresh(api)
    return api


@pytest.mark.asyncio
async def test_first_failure_creates_new_incident(db_session, test_api):
    incident = await incident_service.handle_failed_check(db_session, test_api, "Connection error", 100.0)
    assert incident.status == IncidentStatus.OPEN
    assert incident.failure_count == 1
    assert incident.severity == IncidentSeverity.LOW


@pytest.mark.asyncio
async def test_second_failure_updates_same_incident_not_new_one(db_session, test_api):
    first = await incident_service.handle_failed_check(db_session, test_api, "Error 1", 100.0)
    second = await incident_service.handle_failed_check(db_session, test_api, "Error 2", 100.0)

    assert first.id == second.id  # SAME incident, not a duplicate
    assert second.failure_count == 2
    assert second.severity == IncidentSeverity.MEDIUM


@pytest.mark.asyncio
async def test_successful_check_resolves_open_incident(db_session, test_api):
    incident = await incident_service.handle_failed_check(db_session, test_api, "Error", 100.0)
    assert incident.status == IncidentStatus.OPEN

    resolved = await incident_service.handle_successful_check(db_session, test_api)
    assert resolved.status == IncidentStatus.RESOLVED
    assert resolved.resolved_at is not None
    assert resolved.resolution_time is not None


@pytest.mark.asyncio
async def test_successful_check_with_no_open_incident_does_nothing(db_session, test_api):
    result = await incident_service.handle_successful_check(db_session, test_api)
    assert result is None


@pytest.mark.asyncio
async def test_new_incident_after_resolution_is_separate(db_session, test_api):
    first = await incident_service.handle_failed_check(db_session, test_api, "Error", 100.0)
    await incident_service.handle_successful_check(db_session, test_api)

    second = await incident_service.handle_failed_check(db_session, test_api, "New error", 100.0)
    assert second.id != first.id  # genuinely a new incident, not reopened
    assert second.failure_count == 1