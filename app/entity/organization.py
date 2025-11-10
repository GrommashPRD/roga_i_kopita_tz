from dataclasses import dataclass
from typing import List, Optional
from app.entity.activity import ActivityEntity
from app.entity.building import BuildingEntity


@dataclass
class OrganizationPhoneEntity:
    """
    Entity класс для OrganizationPhone
    """
    id: str
    phone_number: str


@dataclass
class OrganizationEntity:
    """
    Entity класс для Organization
    """
    id: str
    title: str
    building_id: str
    building: Optional[BuildingEntity] = None
    activities: Optional[List[ActivityEntity]] = None
    phones: Optional[List[OrganizationPhoneEntity]] = None

