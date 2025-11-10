from app.entity.protocols import EntityMapper
from app.entity.activity import ActivityEntity
from app.repo.activity.models import Activity


class ActivityMapper(EntityMapper[Activity, ActivityEntity]):
    """
    Маппер для преобразования Activity модели в ActivityEntity
    """
    
    def to_entity(self, model: Activity) -> ActivityEntity:
        """
        Преобразует SQLAlchemy Activity модель в ActivityEntity
        :param model: SQLAlchemy Activity модель
        :return: ActivityEntity объект
        """

        return ActivityEntity(
            id=model.id,
            name=model.name,
            parent_id=model.parent_id,
        )

