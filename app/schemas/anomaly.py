from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AnomalyCheck(BaseModel):
    check_id: int
    checked_at: datetime
    response_time: Optional[float]
    status_code: Optional[int]
    success: bool
    is_anomaly: bool


class AnomalyDetectionResult(BaseModel):
    api_id: int
    total_checks_analyzed: int
    anomalies_found: int
    anomalies: list[AnomalyCheck]