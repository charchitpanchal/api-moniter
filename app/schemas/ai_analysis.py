from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class AiAnalysisOut(BaseModel):
    id: int
    incident_id: int
    severity: str
    probable_cause: str
    evidence: List[str]
    recommendation: List[str]
    summary: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)