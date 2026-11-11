from datetime import UTC, datetime

from app.db.base import Base
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)

    asset_code: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    equipment_type: Mapped[str] = mapped_column(String(100), nullable=False)

    site: Mapped[str] = mapped_column(String(100), nullable=False)

    manufacturer: Mapped[str | None] = mapped_column(String(100))

    model: Mapped[str | None] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    sensors = relationship("Sensor", back_populates="equipment")

    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment")
