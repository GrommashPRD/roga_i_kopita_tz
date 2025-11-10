from pydantic import BaseModel, Field
from typing import List
from app.api.schemas.organization import OrganizationWithBuildingResponse


class RadiusSearchRequest(BaseModel):
    """
    Pydantic схема для поиска по радиусу
    """
    latitude: float = Field(..., ge=-90, le=90, description="Широта центральной точки")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота центральной точки")
    radius_meters: float = Field(..., gt=0, description="Радиус поиска в метрах")


class RectangleSearchRequest(BaseModel):
    """
    Pydantic схема для поиска в прямоугольнике
    """
    min_latitude: float = Field(..., ge=-90, le=90, description="Минимальная широта")
    min_longitude: float = Field(..., ge=-180, le=180, description="Минимальная долгота")
    max_latitude: float = Field(..., ge=-90, le=90, description="Максимальная широта")
    max_longitude: float = Field(..., ge=-180, le=180, description="Максимальная долгота")


class GeoSearchResponse(BaseModel):
    """
    Pydantic схема для ответа
    """
    organizations: List[OrganizationWithBuildingResponse] = Field(default_factory=list, description="Список организаций")

