from pydantic import BaseModel, Field
from typing import List


class IncidentContext(BaseModel):
    """
    Structured input describing an incident, built from database records.
    This is what gets turned into a prompt — never send raw DB objects to an LLM.
    """
    api_name: str
    api_url: str
    expected_status_code: int
    actual_status_code: int | None
    response_time_ms: float | None
    failure_count: int
    recent_errors: List[str]
    incident_duration_seconds: float | None = None


class AIAnalysisResult(BaseModel):
    """
    The structured, validated output we require from the LLM.
    If the LLM's response doesn't match this shape, we treat it as a failure —
    we never store or trust unvalidated free-text from the model.
    """
    severity: str = Field(description="One of LOW, MEDIUM, HIGH, CRITICAL")
    probable_cause: str
    evidence: List[str]
    recommendation: List[str]
    summary: str