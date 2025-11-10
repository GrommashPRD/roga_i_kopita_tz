from dataclasses import dataclass


@dataclass
class BuildingEntity:
    """
    Entity класс для Building
    """
    id: str
    address: str
    latitude: float
    longitude: float

