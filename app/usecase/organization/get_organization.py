from typing import List, Optional
from app.entity.organization import OrganizationEntity
from app.usecase.protocols import IOrganizationRepo
from app.exceptions import NotFoundError, UseCaseExecutionError, DatabaseError


class GetOrganizationUseCase:
    """
    UseCase для получения организаций
    """
    
    def __init__(self, organization_repo: IOrganizationRepo):
        self._organization_repo = organization_repo
    
    async def get_by_id(self, org_id: str) -> OrganizationEntity:
        """
        Получить организацию по ID
        :param org_id: ID организации
        :return: OrganizationEntity объект
        """

        try:
            entity = await self._organization_repo.get_org_by_id(org_id)
        except DatabaseError as e:
            raise UseCaseExecutionError("Error getting organization by id %s: %s" % (org_id, e))
        
        if not entity:
            raise NotFoundError("Organization with id %s not found" % org_id)
        return entity
    
    async def get_by_name(self, organization_name: str) -> List[OrganizationEntity]:
        """
        Получить организации по частичному совпадению названия
        :param organization_name: Часть названия организации для поиска
        :return: Список OrganizationEntity
        """

        try:
            entities = await self._organization_repo.get_org_by_name(organization_name)
        except DatabaseError as e:
            raise UseCaseExecutionError("Error getting organizations by name %s: %s" % (organization_name, e))
        
        if not entities:
            raise NotFoundError("Organizations with name containing %s not found" % organization_name)
        return entities
    
    async def list_by_building(self, building_id: str) -> List[OrganizationEntity]:
        """
        Получить все организации по building_id
        :param building_id: ID здания
        :return: Список организаций
        """

        try:
            entities = await self._organization_repo.list_by_building(building_id)
        except DatabaseError as e:
            raise UseCaseExecutionError("Error getting organizations by building %s: %s" % (building_id, e))
        
        if not entities:
            raise NotFoundError("Organizations for building %s not found" % building_id)
        return entities
    
    async def list_by_activity_exact(self, activity_name: str) -> List[OrganizationEntity]:
        """
        Получить организации по точному названию вида деятельности
        :param activity_name: Название вида деятельности
        :return: Список организаций
        """

        try:
            entities = await self._organization_repo.list_by_activity_exact(activity_name)
        except DatabaseError as e:
            raise UseCaseExecutionError("Error getting organizations by activity %s: %s" % (activity_name, e))
        
        if not entities:
            raise NotFoundError("Organizations for activity %s not found" % activity_name)
        return entities
    
    async def list_by_activity_tree(self, activity_name: str) -> List[OrganizationEntity]:
        """
        Получить организации по виду деятельности с учетом иерархии
        :param activity_name: Название вида деятельности
        :return: Список организаций
        """

        try:
            entities = await self._organization_repo.list_by_activity_hierarchy(activity_name)
        except DatabaseError as e:
            raise UseCaseExecutionError("Error getting organizations by activity tree %s: %s" % (activity_name, e))
        
        if not entities:
            raise NotFoundError("Organizations for activity %s not found" % activity_name)
        return entities

