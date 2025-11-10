from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, cast
from sqlalchemy.exc import SQLAlchemyError
from geoalchemy2 import functions as geo_func
from geoalchemy2.types import Geography
from app.repo.building.models import Building
from app.entity.building import BuildingEntity
from app.entity.mappers.building_mapper import BuildingMapper
from app.exceptions import DatabaseQueryError


class BuildingRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._mapper = BuildingMapper()

    async def list_by_radius(
        self, 
        latitude: float, 
        longitude: float, 
        radius_meters: float
    ) -> list[BuildingEntity]:
        """
        Получить все здания в заданном радиусе от точки
        :param latitude: Широта центральной точки
        :param longitude: Долгота центральной точки
        :param radius_meters: Радиус поиска в метрах
        :return: Список зданий в радиусе
        """

        center_point = geo_func.ST_SetSRID(
            geo_func.ST_MakePoint(longitude, latitude),
            4326
        )

        stmt = (
            select(Building)
            .where(
                geo_func.ST_DWithin(
                    cast(Building.geom, Geography),
                    cast(center_point, Geography),
                    radius_meters
                )
            )
        )
        
        try:
            result = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error listing buildings by radius (lat=%s, lon=%s, radius=%s m): %s"
                                     % (
                                         latitude,
                                         longitude,
                                         radius_meters,
                                         e
                                     )
                                     )

        models = list(result.scalars().all())

        return [self._mapper.to_entity(model) for model in models]

    async def list_by_rectangle(
        self,
        min_latitude: float,
        min_longitude: float,
        max_latitude: float,
        max_longitude: float
    ) -> list[BuildingEntity]:
        """
        Получить все здания в прямоугольной области
        :param min_latitude: Минимальная широта
        :param min_longitude: Минимальная долгота
        :param max_latitude: Максимальная широта
        :param max_longitude: Максимальная долгота
        :return: Список зданий в прямоугольной области
        """

        envelope = geo_func.ST_MakeEnvelope(
            min_longitude,
            min_latitude,
            max_longitude,
            max_latitude,
            4326
        )

        stmt = (
            select(Building)
            .where(
                geo_func.ST_Within(Building.geom, envelope)
            )
        )
        
        try:
            result = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error listing buildings by rectangle (min_lat=%s, min_lon=%s, \
            max_lat=%s, max_lon=%s): %s"
                                     %(
                                         min_latitude,
                                         min_longitude,
                                         max_latitude,
                                         max_longitude,
                                         e
                                     )
                                     )

        models = list(result.scalars().all())

        return [self._mapper.to_entity(model) for model in models]
