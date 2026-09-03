import enum
from datetime import datetime
from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class IncidentStatus(str, enum.Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"


class IncidentSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    api_id: Mapped[int] = mapped_column(ForeignKey("monitored_apis.id"), nullable=False)

    status: Mapped[IncidentStatus] = mapped_column(Enum(IncidentStatus), default=IncidentStatus.OPEN, nullable=False)
    severity: Mapped[IncidentSeverity] = mapped_column(Enum(IncidentSeverity), default=IncidentSeverity.LOW, nullable=False)
    failure_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resolution_time: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    api: Mapped["MonitoredApi"] = relationship(back_populates="incidents")
    ai_analyses: Mapped[list["AiAnalysis"]] = relationship(back_populates="incident", cascade="all, delete-orphan")