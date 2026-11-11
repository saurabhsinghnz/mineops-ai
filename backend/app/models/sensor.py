from app.db.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Sensor(Base):
    __tablename__ = "sensor"

    id: Mapped[int] = mapped_column(primary_key=True)

    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id"), nullable=False
    )

    sensor_type: Mapped[str] = mapped_column(String(100), nullable=False)

    unit: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str | None] = mapped_column(String(255))

    equipment = relationship("Equipment", back_populates="sensors")

    telemetry = relationship("Telemetry", back_populates="sensor")
