from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ApiCheckOut(BaseModel):
    id: int
    api_id: int
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    success: bool
    error_message: Optional[str] = None
    timeout: bool
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)