from app.services.incident_service import determine_severity
from app.models.incident import IncidentSeverity


def test_severity_low_on_first_failure():
    assert determine_severity(1, 100.0, None) == IncidentSeverity.LOW


def test_severity_medium_at_two_failures():
    assert determine_severity(2, 100.0, None) == IncidentSeverity.MEDIUM


def test_severity_medium_at_three_failures():
    assert determine_severity(3, 100.0, None) == IncidentSeverity.MEDIUM


def test_severity_high_at_four_failures():
    assert determine_severity(4, 100.0, None) == IncidentSeverity.HIGH


def test_severity_high_at_five_failures():
    assert determine_severity(5, 100.0, None) == IncidentSeverity.HIGH


def test_severity_critical_at_six_failures():
    assert determine_severity(6, 100.0, None) == IncidentSeverity.CRITICAL


def test_severity_critical_stays_critical_at_high_counts():
    assert determine_severity(100, 100.0, None) == IncidentSeverity.CRITICAL