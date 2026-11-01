from fastapi import APIRouter, HTTPException

from app.schemas.equipment import EquipmentResponse
from app.services.equipment_service import (
    get_all_equipment,
    get_equipment_by_id
)

router = APIRouter(
    prefix="/api/v1/equipment",
    tags=["Equipment"]
)


@router.get("", response_model=list[EquipmentResponse])
def list_equipment():
    return get_all_equipment()


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def retrieve_equipment(equipment_id: int):

    equipment = get_equipment_by_id(equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    return equipment
