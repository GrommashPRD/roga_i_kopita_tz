from app.entity.organization import OrganizationEntity
from app.entity.building import BuildingEntity
from app.api.schemas.organization import (
    OrganizationResponse,
    OrganizationPhoneResponse,
    OrganizationSimpleResponse,
    OrganizationWithBuildingResponse
)
from app.api.schemas.building import BuildingResponse
from app.api.schemas.activity import ActivityResponse


def organization_entity_to_response(entity: OrganizationEntity) -> OrganizationResponse:
    """
    Преобразование данных в Response объект
    :param entity: OrganizationEntity объект
    :return: OrganizationResponse объект
    """
    building_response = None
    if entity.building:
        building_response = BuildingResponse(
            id=entity.building.id,
            address=entity.building.address,
            latitude=entity.building.latitude,
            longitude=entity.building.longitude,
        )
    

    activities_response = None
    if entity.activities:
        activities_response = [
            ActivityResponse(
                id=activity.id,
                name=activity.name,
                parent_id=activity.parent_id,
            )
            for activity in entity.activities
        ]

    phones_response = None
    if entity.phones:
        phones_response = [
            OrganizationPhoneResponse(
                id=phone.id,
                phone_number=phone.phone_number,
            )
            for phone in entity.phones
        ]
    
    return OrganizationResponse(
        id=entity.id,
        title=entity.title,
        building_id=entity.building_id,
        building=building_response,
        activities=activities_response,
        phones=phones_response,
    )


def organization_entity_to_simple_response(entity: OrganizationEntity) -> OrganizationSimpleResponse:
    """
    Преобразование данных OrganizationEntity в Response объект, только название и телефон.
    :param entity: OrganizationEntity объект
    :return: OrganizationSimpleResponse объект
    """

    phone_numbers = []
    if entity.phones:
        phone_numbers = [phone.phone_number for phone in entity.phones]
    
    return OrganizationSimpleResponse(
        title=entity.title,
        phones=phone_numbers,
    )


def organization_entity_to_with_building_response(entity: OrganizationEntity) -> OrganizationWithBuildingResponse:
    """
    Преобразрование данных OrganizationEntity в Response объект, название, телефон и здание
    :param entity: OrganizationEntity объект
    :return: OrganizationWithBuildingResponse объект
    """

    phone_numbers = []
    if entity.phones:
        phone_numbers = [phone.phone_number for phone in entity.phones]

    building_response = None
    if entity.building:
        building_response = BuildingResponse(
            id=entity.building.id,
            address=entity.building.address,
            latitude=entity.building.latitude,
            longitude=entity.building.longitude,
        )
    
    return OrganizationWithBuildingResponse(
        title=entity.title,
        phones=phone_numbers,
        building=building_response,
    )


def building_entity_to_response(entity: BuildingEntity) -> BuildingResponse:
    """
    Преобразование BuildingEntity в Response объект
    :param entity: BuildingEntity объект
    :return: BuildingResponse объект
    """

    return BuildingResponse(
        id=entity.id,
        address=entity.address,
        latitude=entity.latitude,
        longitude=entity.longitude,
    )

