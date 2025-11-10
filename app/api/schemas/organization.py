from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.api.schemas.activity import ActivityResponse
from app.api.schemas.building import BuildingResponse


class OrganizationPhoneResponse(BaseModel):
    """
    Pydantic схема для OrganizationPhone
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    phone_number: str


class OrganizationResponse(BaseModel):
    """
    Pydantic схема для Organization
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    title: str
    building_id: str
    building: Optional[BuildingResponse] = None
    activities: Optional[List[ActivityResponse]] = None
    phones: Optional[List[OrganizationPhoneResponse]] = None


class OrganizationSimpleResponse(BaseModel):
    """
    Pydantic схема для Organization, только название и телефон
    """
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    phones: List[str] = []


class OrganizationWithBuildingResponse(BaseModel):
    """
    Pydantic схема для Organization, только название, телефон и здание
    """
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    phones: List[str] = []
    building: Optional[BuildingResponse] = None
