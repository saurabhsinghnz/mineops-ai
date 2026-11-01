from pydantic import BaseModel


class EquipmentResponse(BaseModel):
    id: int
    asset_code: str
    name: str
    equipment_type: str
    site: str
    manufacturer: str
    model: str
