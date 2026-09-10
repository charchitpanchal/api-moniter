from datetime import datetime
from sqlalchemy import Integer, Float, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class ApiCheck(Base):
    __tablename__ = "api_checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    api_id: Mapped[int] = mapped_column(ForeignKey("monitored_apis.id"), nullable=False)

    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    timeout: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    api: Mapped["MonitoredApi"] = relationship(back_populates="checks")