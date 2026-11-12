from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate
from sqlalchemy import select
from sqlalchemy.orm import Session


def create_equipment(db: Session, data: EquipmentCreate) -> Equipment:
    equipment = Equipment(**data.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


def get_all_equipment(db: Session) -> list[Equipment]:
    return list(db.scalars(select(Equipment)))


def get_equipment_by_id(db: Session, equipment_id: int) -> Equipment | None:
    return db.get(Equipment, equipment_id)
