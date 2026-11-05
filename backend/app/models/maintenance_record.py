from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_record"

    id: Mapped[int] = mapped_column(primary_key=True)

    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id"), nullable=False
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    summary: Mapped[str] = mapped_column(nullable=False)

    action_taken: Mapped[str] = mapped_column(nullable=False)

    source: Mapped[str] = mapped_column(nullable=False)

    equipment = relationship("Equipment", back_populates="maintenance_records")
