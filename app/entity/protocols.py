from typing import Protocol, TypeVar, Generic

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")


class EntityMapper(Protocol, Generic[TModel, TEntity]):
    """
    Protocol для контракта маппера, который преобразует SQLAlchemy модели в Entity объекты
    """
    
    def to_entity(self, model: TModel) -> TEntity:
        """
        Преобразует SQLAlchemy модель в Entity объект
        :param model: SQLAlchemy модель
        :return: Entity объект
        """

        ...

