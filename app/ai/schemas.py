from pydantic import BaseModel, Field
from typing import List


class IncidentContext(BaseModel):
    api_name: str
    api_url: str
    expected_status_code: int
    actual_status_code: int | None
    response_time_ms: float | None
    failure_count: int
    recent_errors: List[str]
    incident_duration_seconds: float | None = None


class AIAnalysisResult(BaseModel):
    severity: str = Field(description="One of LOW, MEDIUM, HIGH, CRITICAL")
    probable_cause: str
    evidence: List[str]
    recommendation: List[str]
    summary: str


class SummaryResult(BaseModel):
    """Lightweight output for the summarization feature — just plain text."""
    summary: str