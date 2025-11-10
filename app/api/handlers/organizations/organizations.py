from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from app.api.dependencies import (
    verify_api_key,
    get_organization_use_case,
    get_geo_search_use_case
)
from app.usecase.organization.get_organization import GetOrganizationUseCase
from app.usecase.geo_search.search_use_case import GeoSearchUseCase
from app.api.schemas.organization import OrganizationResponse, OrganizationSimpleResponse
from app.api.schemas.geo_search import GeoSearchResponse
from app.api.schemas.mappers import (
    organization_entity_to_response,
    organization_entity_to_simple_response,
    organization_entity_to_with_building_response,
)
from app.exceptions import NotFoundError, UseCaseExecutionError, DatabaseError
from app.logger import logger


router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/by-building/{building_id}",
    response_model=List[OrganizationSimpleResponse]
)
async def get_organizations_by_building(
        building_id: str,
        use_case: GetOrganizationUseCase = Depends(get_organization_use_case)
) -> List[OrganizationSimpleResponse]:
    """
    handler поиска организаций по ID здания
    :param building_id: ID здания
    :param use_case: Бизнес-логика для выполнения поиска организаций.
    :return: Объект ответа, содержащий список найденных организаций.
    """
    try:
        entities = await use_case.list_by_building(building_id)
    except NotFoundError as e:
        logger.warning("Failed to get organizations by building id: %s", building_id)
        raise HTTPException(status_code=404, detail=str(e))
    except (UseCaseExecutionError, DatabaseError) as e:
        logger.error("Error getting organizations by building id: %s", building_id, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return [organization_entity_to_simple_response(entity) for entity in entities]


@router.get(
    "/by-activity/exact",
    response_model=List[OrganizationSimpleResponse]
)
async def get_organizations_by_activity_exact(
    activity_name: str = Query(..., description="Название вида деятельности для поиска"),
    use_case: GetOrganizationUseCase = Depends(get_organization_use_case)
) -> List[OrganizationSimpleResponse]:
    """
    Получить организации, относящиеся только к указанному виду деятельности.
    :param activity_name: Название активности
    :param use_case: Бизнес-логика для выполнения поиска по активности.
    :return: Объект ответа, содержащий список найденных организаций.
    """
    try:
        entities = await use_case.list_by_activity_exact(activity_name)
    except NotFoundError as e:
        logger.warning("Failed to get organizations by activity name: %s", activity_name)
        raise HTTPException(status_code=404, detail=str(e))
    except (UseCaseExecutionError, DatabaseError) as e:
        logger.error("Error getting organizations by activity name: %s", activity_name, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return [organization_entity_to_simple_response(entity) for entity in entities]


@router.get(
    "/by-activity/tree",
    response_model=List[OrganizationSimpleResponse]
)
async def get_organizations_by_activity_tree(
    activity_name: str = Query(..., description="Название вида деятельности для поиска с учетом иерархии"),
    use_case: GetOrganizationUseCase = Depends(get_organization_use_case)
) -> List[OrganizationSimpleResponse]:
    """
    Получить организации, относящиеся к указанному виду деятельности,
    а также к его дочерним и родительским видам.
    :param activity_name: Название вида деятельности
    :param use_case: Бизнес-логика для выполнения роиска по активности.
    :return: Объект ответа, содержащий список найденных организаций.
    """
    try:
        entities = await use_case.list_by_activity_tree(activity_name)
    except NotFoundError as e:
        logger.warning("Failed to get organizations by activity tree: %s", activity_name)
        raise HTTPException(status_code=404, detail=str(e))
    except (UseCaseExecutionError, DatabaseError) as e:
        logger.error("Error getting organizations by activity tree: %s", activity_name, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return [organization_entity_to_simple_response(entity) for entity in entities]


@router.get(
    "/search/radius",
    response_model=GeoSearchResponse
)
async def search_by_radius(
        latitude: float = Query(..., ge=-90, le=90, description="Широта центральной точки"),
        longitude: float = Query(..., ge=-180, le=180, description="Долгота центральной точки"),
        radius_meters: float = Query(..., gt=0, description="Радиус поиска в метрах"),
        use_case: GeoSearchUseCase = Depends(get_geo_search_use_case)
) -> GeoSearchResponse:
    """
    Поиск организаций в заданном радиусе от указанной географической точки.
    :param latitude: Широта центральной точки поиска.
    :param longitude: Долгота центральной точки поиска.
    :param radius_meters: Радиус поиска в метрах.
    :param use_case:Бизнес-логика для выполнения геопоиска.
    :return: Объект ответа, содержащий список найденных организаций.
    """
    try:
        org_entities, _ = await use_case.search_by_radius(
            latitude,
            longitude,
            radius_meters
        )
    except (UseCaseExecutionError, DatabaseError) as e:
        logger.error("Error searching by radius: lat=%s, lon=%s, radius=%s", latitude, longitude, radius_meters, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

    organizations = [organization_entity_to_with_building_response(entity) for entity in org_entities]

    return GeoSearchResponse(
        organizations=organizations
    )


@router.get(
    "/search/rectangle",
    response_model=GeoSearchResponse
)
async def search_by_rectangle(
        min_latitude: float = Query(..., ge=-90, le=90, description="Минимальная широта"),
        min_longitude: float = Query(..., ge=-180, le=180, description="Минимальная долгота"),
        max_latitude: float = Query(..., ge=-90, le=90, description="Максимальная широта"),
        max_longitude: float = Query(..., ge=-180, le=180, description="Максимальная долгота"),
        use_case: GeoSearchUseCase = Depends(get_geo_search_use_case)
) -> GeoSearchResponse:
    """
    Поиск организаций в заданной прямоугольной области на карте.
    :param min_latitude: Минимальная широта
    :param min_longitude: Минимальная долгота
    :param max_latitude: Максимальная широта
    :param max_longitude: Максимальная долгота
    :param use_case: Бизнес‑логика для выполнения геопоиска.
    :return: Объект ответа, содержащий список найденных организаций
    """
    try:
        org_entities, _ = await use_case.search_by_rectangle(
            min_latitude,
            min_longitude,
            max_latitude,
            max_longitude
        )
    except (UseCaseExecutionError, DatabaseError) as e:
        logger.error("Error searching by rectangle: min_lat=%s, min_lon=%s, max_lat=%s, max_lon=%s", 
                    min_latitude, min_longitude, max_latitude, max_longitude, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

    organizations = [organization_entity_to_with_building_response(entity) for entity in org_entities]

    return GeoSearchResponse(
        organizations=organizations
    )

@router.get(
    "/by-name",
    response_model=List[OrganizationResponse]
)
async def get_org_by_name(
    organization_name: str = Query(..., description="Часть названия организации для поиска"),
    use_case: GetOrganizationUseCase = Depends(get_organization_use_case)
) -> List[OrganizationResponse]:
    """
    Поиск организаций по части названия.
    :param organization_name: Подстрока для поиска в названиях организаций.
    :param use_case: Бизнес‑логика для получения организаций.
    :return: Список объектов организаций, соответствующих критериям поиска.
    """
    try:
        entities = await use_case.get_by_name(organization_name)
    except NotFoundError as e:
        logger.warning("Failed to get organizations by name: %s", organization_name)
        raise HTTPException(status_code=404, detail=str(e))
    except (UseCaseExecutionError, DatabaseError) as e:
        logger.error("Error getting organizations by name: %s", organization_name, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return [organization_entity_to_response(entity) for entity in entities]

@router.get(
    "/{org_id}",
    response_model=OrganizationResponse
)
async def get_org_by_id(
        org_id: str,
        use_case: GetOrganizationUseCase = Depends(get_organization_use_case)
)-> OrganizationResponse:
    """
    Получает информацию об организации по её уникальному идентификатору.
    :param org_id: Уникальный идентификатор организации.
    :param use_case: Бизнес‑логика для получения данных организации.
    :return: Объект с полной информацией об организации.
    """
    try:
        entity = await use_case.get_by_id(org_id)
    except NotFoundError as e:
        logger.warning("Failed to get organization by id: %s", org_id)
        raise HTTPException(status_code=404, detail=str(e))
    except (UseCaseExecutionError, DatabaseError) as e:
        logger.error("Error getting organization by id: %s", org_id, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return organization_entity_to_response(entity)