from pydantic import BaseModel, ConfigDict


class BuildingResponse(BaseModel):
    """
    Pydantic схема для Building
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    address: str
    latitude: float
    longitude: float

