from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.incident import IncidentStatus, IncidentSeverity


class IncidentOut(BaseModel):
    id: int
    api_id: int
    status: IncidentStatus
    severity: IncidentSeverity
    failure_count: int
    started_at: datetime
    resolved_at: Optional[datetime] = None
    last_error: Optional[str] = None
    resolution_time: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus] = None