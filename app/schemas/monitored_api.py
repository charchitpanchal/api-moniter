from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field, field_validator, ConfigDict

VALID_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}


class MonitoredApiCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    url: HttpUrl
    method: str = "GET"
    expected_status_code: int = Field(default=200, ge=100, le=599)
    monitoring_interval: int = Field(default=60, gt=0, description="Seconds between checks")
    timeout: int = Field(default=5, gt=0, description="Seconds before timing out")
    headers: Optional[dict] = None
    request_body: Optional[dict] = None

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        v = v.upper()
        if v not in VALID_METHODS:
            raise ValueError(f"method must be one of {VALID_METHODS}")
        return v


class MonitoredApiUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=150)
    url: Optional[HttpUrl] = None
    method: Optional[str] = None
    expected_status_code: Optional[int] = Field(default=None, ge=100, le=599)
    monitoring_interval: Optional[int] = Field(default=None, gt=0)
    timeout: Optional[int] = Field(default=None, gt=0)
    active: Optional[bool] = None
    headers: Optional[dict] = None
    request_body: Optional[dict] = None

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.upper()
        if v not in VALID_METHODS:
            raise ValueError(f"method must be one of {VALID_METHODS}")
        return v


class MonitoredApiOut(BaseModel):
    id: int
    user_id: int
    name: str
    url: str
    method: str
    expected_status_code: int
    monitoring_interval: int
    timeout: int
    active: bool
    headers: Optional[dict] = None
    request_body: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)