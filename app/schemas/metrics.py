from pydantic import BaseModel
from typing import Optional


class ApiMetrics(BaseModel):
    api_id: int
    total_checks: int
    successful_checks: int
    failed_checks: int
    uptime_percentage: float
    error_rate: float
    average_response_time: Optional[float] = None
    min_response_time: Optional[float] = None
    max_response_time: Optional[float] = None


class ApiStatus(BaseModel):
    api_id: int
    active: bool
    last_check_success: Optional[bool] = None
    last_checked_at: Optional[str] = None
    current_status: str  # "HEALTHY" | "DOWN" | "UNKNOWN"