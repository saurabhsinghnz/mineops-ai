from app.db.session import SessionLocal
from app.models.equipment import Equipment
from sqlalchemy import select

with SessionLocal() as db:
    statement = select(Equipment).where(Equipment.asset_code == "HT-102")

    equipment = db.scalar(statement)

    print(equipment.name if equipment else None)
