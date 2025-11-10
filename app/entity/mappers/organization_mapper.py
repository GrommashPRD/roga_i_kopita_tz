from typing import List, Optional
from app.entity.protocols import EntityMapper
from app.entity.organization import OrganizationEntity, OrganizationPhoneEntity
from app.entity.activity import ActivityEntity
from app.entity.building import BuildingEntity
from app.repo.organization.models import Organization, OrganizationPhone
from app.entity.mappers.activity_mapper import ActivityMapper
from app.entity.mappers.building_mapper import BuildingMapper


class OrganizationMapper(EntityMapper[Organization, OrganizationEntity]):
    """
    Маппер для преобразования Organization модели в OrganizationEntity
    """
    
    def __init__(self):
        self._activity_mapper = ActivityMapper()
        self._building_mapper = BuildingMapper()
    
    def to_entity(self, model: Organization) -> OrganizationEntity:
        """
        Преобразует SQLAlchemy Organization модель в OrganizationEntity
        :param model: SQLAlchemy Organization модель
        :return: OrganizationEntity объект
        """

        building: Optional[BuildingEntity] = None
        if model.building:
            building = self._building_mapper.to_entity(model.building)
        

        activities: Optional[List[ActivityEntity]] = None
        if model.activities:
            activities = [self._activity_mapper.to_entity(activity) for activity in model.activities]
        

        phones: Optional[List[OrganizationPhoneEntity]] = None
        if model.phones:
            phones = [
                OrganizationPhoneEntity(
                    id=phone.id,
                    phone_number=phone.phone_number,
                )
                for phone in model.phones
            ]
        
        return OrganizationEntity(
            id=model.id,
            title=model.title,
            building_id=model.building_id,
            building=building,
            activities=activities,
            phones=phones,
        )

