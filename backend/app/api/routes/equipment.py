from typing import Annotated

from app.api.dependencies import get_db
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentResponse
from app.services.service import (
    create_equipment,
    get_all_equipment,
    get_equipment_by_id,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/equipment", tags=["Equipment"])


@router.post("", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
def add_equipment(data: EquipmentCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        return create_equipment(db, data)
    except IntegrityError:
        db.rollback()
        existing = db.scalar(
            select(Equipment.id).where(Equipment.asset_code == data.asset_code)
        )
        if existing is not None:
            raise HTTPException(status_code=409, detail="Asset code already exists")
        raise


@router.get("", response_model=list[EquipmentResponse])
def list_equipment():
    return get_all_equipment()


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def retrieve_equipment(equipment_id: int):

    equipment = get_equipment_by_id(equipment_id)

    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return equipment
