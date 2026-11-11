from pydantic import BaseModel, ConfigDict


class EquipmentCreate(BaseModel):
    asset_code: str
    name: str
    equipment_type: str
    site: str
    manufacturer: str | None = None
    model: str | None = None


class EquipmentResponse(BaseModel):
    id: int
    asset_code: str
    name: str
    equipment_type: str
    site: str
    manufacturer: str | None
    model: str | None

    model_config = ConfigDict(from_attributes=True)
