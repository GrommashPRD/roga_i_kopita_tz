from typing import Tuple, List
from app.entity.organization import OrganizationEntity
from app.entity.building import BuildingEntity
from app.usecase.protocols import IOrganizationRepo, IBuildingRepo
from app.exceptions import UseCaseExecutionError, DatabaseError


class GeoSearchUseCase:
    """
    UseCase для поиска организаций и зданий
    """
    
    def __init__(
        self,
        organization_repo: IOrganizationRepo,
        building_repo: IBuildingRepo
    ):
        self._organization_repo = organization_repo
        self._building_repo = building_repo
    
    async def search_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_meters: float
    ) -> Tuple[List[OrganizationEntity], List[BuildingEntity]]:
        """
        Поиск организаций и зданий в заданном радиусе от точки
        :param latitude:  Широта центральной точки
        :param longitude: Долгота центральной точки
        :param radius_meters: Радиус поиска в метрах
        :return: tuple - список организаций, список зданий
        """

        try:
            org_entities = await self._organization_repo.list_by_radius(
                latitude,
                longitude,
                radius_meters
            )
        except DatabaseError as e:
            raise UseCaseExecutionError(
                "Error searching organizations by radius (lat=%f, lon=%f, radius=%f m): %s"
                %(
                    latitude,
                    longitude,
                    radius_meters,
                    e
                )
            )
        
        try:
            building_entities = await self._building_repo.list_by_radius(
                latitude,
                longitude,
                radius_meters
            )
        except DatabaseError as e:
            raise UseCaseExecutionError(
                "Error searching organizations by radius (lat=%f, lon=%f, radius=%f m): %s"
                %(
                    latitude,
                    longitude,
                    radius_meters,
                    e
                )
            )
        
        return org_entities, building_entities
    
    async def search_by_rectangle(
        self,
        min_latitude: float,
        min_longitude: float,
        max_latitude: float,
        max_longitude: float
    ) -> Tuple[List[OrganizationEntity], List[BuildingEntity]]:
        """
        Поиск организаций и зданий в прямоугольной области
        :param min_latitude: max широта
        :param min_longitude: min долгота
        :param max_latitude: max широта
        :param max_longitude: max долгота
        :return: tuple организаций, tuple зданий
        """

        try:
            org_entities = await self._organization_repo.list_by_rectangle(
                min_latitude,
                min_longitude,
                max_latitude,
                max_longitude
            )
        except DatabaseError as e:
            raise UseCaseExecutionError(
                "Error searching organizations by rectangle (min_lat=%f, min_lon=%f, max_lat=%f, max_lon=%f): %s"
                %(
                    min_latitude,
                    min_longitude,
                    max_latitude,
                    max_longitude,
                    e
                )
            )

        
        try:
            building_entities = await self._building_repo.list_by_rectangle(
                min_latitude,
                min_longitude,
                max_latitude,
                max_longitude
            )
        except DatabaseError as e:
            raise UseCaseExecutionError(
                "Error searching organizations by rectangle (min_lat=%f, min_lon=%f, max_lat=%f, max_lon=%f): %s"
                %(
                    min_latitude,
                    min_longitude,
                    max_latitude,
                    max_longitude,
                    e
                )
            )
        
        return org_entities, building_entities

