equipment_data = [
    {
        "id": 1,
        "asset_code": "HT-102",
        "name": "Haul Truck 102",
        "equipment_type": "Haul Truck",
        "site": "Site A",
        "manufacturer": "Caterpillar",
        "model": "793F"
    },
    {
        "id": 2,
        "asset_code": "PMP-201",
        "name": "Water Pump 201",
        "equipment_type": "Water Pump",
        "site": "Site A",
        "manufacturer": "Grundfos",
        "model": "CR64"
    }
]


def get_all_equipment():
    return equipment_data


def get_equipment_by_id(equipment_id: int):
    for equipment in equipment_data:
        if equipment["id"] == equipment_id:
            return equipment

    return None
