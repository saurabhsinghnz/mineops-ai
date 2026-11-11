from app.db.session import SessionLocal
from app.models.equipment import Equipment

with SessionLocal() as db:
    equipment = Equipment(
        asset_code="HT-102",
        name="Haul Truck 102",
        equipment_type="Haul Truck",
        site="Pilbara",
        manufacturer="Caterpillar",
        model="793F",
    )

    db.add(equipment)
    db.commit()
    db.refresh(equipment)

    print(equipment.id)
