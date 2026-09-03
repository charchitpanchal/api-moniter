from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class MonitoredApi(Base):
    __tablename__ = "monitored_apis"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    method: Mapped[str] = mapped_column(String(10), default="GET", nullable=False)
    expected_status_code: Mapped[int] = mapped_column(Integer, default=200, nullable=False)
    monitoring_interval: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    timeout: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    headers: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    request_body: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner: Mapped["User"] = relationship(back_populates="monitored_apis")
    checks: Mapped[list["ApiCheck"]] = relationship(back_populates="api", cascade="all, delete-orphan")
    incidents: Mapped[list["Incident"]] = relationship(back_populates="api", cascade="all, delete-orphan")