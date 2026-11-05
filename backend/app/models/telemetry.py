from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id"), nullable=False)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    value: Mapped[float] = mapped_column(Float, nullable=False)

    sensor = relationship("Sensor", back_populates="telemetry")
