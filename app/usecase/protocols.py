from typing import Protocol, List, Optional
from app.entity.organization import OrganizationEntity
from app.entity.building import BuildingEntity


class IOrganizationRepo(Protocol):
    """Протокол для репозитория организаций"""
    
    async def get_org_by_id(self, org_id: str) -> Optional[OrganizationEntity]:
        """Получить организацию по ID"""
        ...
    
    async def get_org_by_name(self, organization_name: str) -> List[OrganizationEntity]:
        """Получить организации по частичному совпадению названия"""
        ...
    
    async def list_by_building(self, building_id: str) -> List[OrganizationEntity]:
        """Получить все организации по building_id"""
        ...
    
    async def list_by_activity_exact(self, activity_name: str) -> List[OrganizationEntity]:
        """Получить организации по точному названию вида деятельности"""
        ...
    
    async def list_by_activity_hierarchy(self, activity_name: str) -> List[OrganizationEntity]:
        """Получить организации по виду деятельности с учетом иерархии"""
        ...
    
    async def list_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_meters: float
    ) -> List[OrganizationEntity]:
        """Получить организации в радиусе"""
        ...
    
    async def list_by_rectangle(
        self,
        min_latitude: float,
        min_longitude: float,
        max_latitude: float,
        max_longitude: float
    ) -> List[OrganizationEntity]:
        """Получить организации в прямоугольной области"""
        ...


class IBuildingRepo(Protocol):
    """Протокол для репозитория зданий"""
    
    async def list_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_meters: float
    ) -> List[BuildingEntity]:
        """Получить здания в радиусе"""
        ...
    
    async def list_by_rectangle(
        self,
        min_latitude: float,
        min_longitude: float,
        max_latitude: float,
        max_longitude: float
    ) -> List[BuildingEntity]:
        """Получить здания в прямоугольной области"""
        ...

