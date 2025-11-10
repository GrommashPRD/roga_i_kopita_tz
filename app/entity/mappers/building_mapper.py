from app.entity.protocols import EntityMapper
from app.entity.building import BuildingEntity
from app.repo.building.models import Building


class BuildingMapper(EntityMapper[Building, BuildingEntity]):
    """
    Маппер для преобразования Building модели в BuildingEntity
    """
    
    def to_entity(self, model: Building) -> BuildingEntity:
        """
        Преобразует SQLAlchemy Building модель в BuildingEntity
        :param model: SQLAlchemy Building модель
        :return: BuildingEntity объект
        """

        return BuildingEntity(
            id=model.id,
            address=model.address,
            latitude=model.latitude,
            longitude=model.longitude,
        )

