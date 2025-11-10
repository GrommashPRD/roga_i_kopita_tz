from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, cast
from sqlalchemy.orm import selectinload, aliased
from sqlalchemy.sql import func, literal
from sqlalchemy.exc import SQLAlchemyError
from geoalchemy2 import functions as geo_func
from geoalchemy2.types import Geography
from app.repo.organization.models import Organization, organization_activities
from app.repo.activity.models import Activity
from app.repo.building.models import Building
from app.entity.organization import OrganizationEntity
from app.entity.mappers.organization_mapper import OrganizationMapper
from app.exceptions import DatabaseQueryError


class OrganizationRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._mapper = OrganizationMapper()

    async def get_org_by_id(self, org_id: str):
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
            .where(Organization.id == org_id)
        )

        try:
            result = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error getting organization by id %s: %s" % (org_id, e))

        model = result.scalars().first()

        if not model:
            return None

        return self._mapper.to_entity(model)


    async def get_org_by_name(self, organization_name: str) -> list[OrganizationEntity]:
        """
        Получить организации по частичному совпадению названия (case-insensitive)
        :param organization_name: Часть названия организации для поиска
        :return: Список организаций, название которых содержит указанную строку
        """

        normalized_name = organization_name.strip().lower()
        if not normalized_name:
            return []
        

        search_pattern = f"%{normalized_name}%"
        
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .where(func.lower(Organization.title).like(search_pattern))
        )

        try:
            result = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error getting organizations by name %s: %s" % (organization_name, e))

        models = list(result.scalars().all())

        # Преобразуем модели в Entity объекты
        return [self._mapper.to_entity(model) for model in models]

    async def list_by_building(self, building_id: str) -> list[OrganizationEntity]:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .where(Organization.building_id == building_id)
        )
        
        try:
            result = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error listing organizations by building %s: %s" %(building_id, e))

        models = list(result.scalars().all())

        return [self._mapper.to_entity(model) for model in models]

    async def list_by_activity_exact(self, activity_name: str) -> list[OrganizationEntity]:
        normalized_name = activity_name.strip().lower()
        if not normalized_name:
            return []

        stmt = (
            select(Organization)
            .distinct()
            .join(organization_activities, Organization.id == organization_activities.c.organization_id)
            .join(Activity, organization_activities.c.activity_id == Activity.id)
            .where(func.lower(Activity.name) == normalized_name)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
        )

        try:
            result = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error listing organizations by activity exact %s: %s" % (activity_name, e))

        models = list(result.scalars().all())

        return [self._mapper.to_entity(model) for model in models]

    async def list_by_activity_hierarchy(self, activity_name: str) -> list[OrganizationEntity]:
        normalized_name = activity_name.strip().lower()
        if not normalized_name:
            return []

        base_select = select(
            Activity.id,
            Activity.parent_id,
            literal(0).label('level')
        ).where(func.lower(Activity.name) == normalized_name)

        descendants_cte = base_select.cte(name="activity_descendants", recursive=True)
        descendant_alias = aliased(Activity)
        descendants_cte = descendants_cte.union_all(
            select(
                descendant_alias.id,
                descendant_alias.parent_id,
                (descendants_cte.c.level + 1).label('level')
            )
            .where(
                descendant_alias.parent_id == descendants_cte.c.id,
                descendants_cte.c.level < 2
            )
        )

        ancestors_base_select = select(
            Activity.id,
            Activity.parent_id,
            literal(0).label('level')
        ).where(func.lower(Activity.name) == normalized_name)
        ancestors_cte = ancestors_base_select.cte(name="activity_ancestors", recursive=True)
        ancestor_alias = aliased(Activity)
        ancestors_cte = ancestors_cte.union_all(
            select(
                ancestor_alias.id,
                ancestor_alias.parent_id,
                (ancestors_cte.c.level + 1).label('level')
            )
            .where(
                ancestor_alias.id == ancestors_cte.c.parent_id,
                ancestors_cte.c.level < 2
            )
        )

        try:
            descendants_result = await self.session.execute(select(descendants_cte.c.id))
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error listing organizations by activity hierarchy %s: %s" % (activity_name, e))

        try:
            ancestors_result = await self.session.execute(select(ancestors_cte.c.id))
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error listing organizations by activity hierarchy %s: %s" % (activity_name, e))

        activity_ids = set(descendants_result.scalars().all()) | set(ancestors_result.scalars().all())

        if not activity_ids:
            return []

        stmt = (
            select(Organization)
            .distinct()
            .join(organization_activities, Organization.id == organization_activities.c.organization_id)
            .where(organization_activities.c.activity_id.in_(activity_ids))
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
        )

        try:
            result = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error listing organizations by activity hierarchy %s: %s" % (activity_name, e))

        models = list(result.scalars().all())

        return [self._mapper.to_entity(model) for model in models]

    async def list_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_meters: float
    ) -> list[OrganizationEntity]:
        center_point = geo_func.ST_SetSRID(
            geo_func.ST_MakePoint(longitude, latitude),
            4326
        )

        stmt = (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .where(
                geo_func.ST_DWithin(
                    cast(Building.geom, Geography),
                    cast(center_point, Geography),
                    radius_meters
                )
            )
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
        )
        
        try:
            result = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error listing organizations by radius (lat=%s, lon=%s, radius=%s m): %s"
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
    ) -> list[OrganizationEntity]:
        envelope = geo_func.ST_MakeEnvelope(
            min_longitude,
            min_latitude,
            max_longitude,
            max_latitude,
            4326
        )

        stmt = (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .where(
                geo_func.ST_Within(Building.geom, envelope)
            )
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
        )
        
        try:
            result = await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error listing organizations by rectangle (min_lat=%s, min_lon=%s, \
            max_lat=%s, max_lon=%s): %s"
                                     % (
                                         min_latitude,
                                         min_longitude,
                                         max_latitude,
                                         max_longitude,
                                         e
                                     )
                                     )

        models = list(result.scalars().all())

        return [self._mapper.to_entity(model) for model in models]
