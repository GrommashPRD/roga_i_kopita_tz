import pytest
from typing import List
from app.entity.organization import OrganizationEntity, OrganizationPhoneEntity
from app.entity.building import BuildingEntity
from app.entity.activity import ActivityEntity


@pytest.fixture
def sample_building_entity() -> BuildingEntity:
    """
    Фикстура для создания тестового BuildingEntity
    """
    return BuildingEntity(
        id="building-1",
        address="Москва, ул. Тестовая, д. 1",
        latitude=55.7558,
        longitude=37.6173
    )


@pytest.fixture
def sample_activity_entity() -> ActivityEntity:
    """
    Фикстура для создания тестового ActivityEntity
    """
    return ActivityEntity(
        id=1,
        name="Розничная торговля",
        parent_id=None
    )


@pytest.fixture
def sample_phone_entities() -> List[OrganizationPhoneEntity]:
    """
    Фикстура для создания списка тестовых OrganizationPhoneEntity
    """
    return [
        OrganizationPhoneEntity(
            id="phone-1",
            phone_number="+7 123 456 7890"
        ),
        OrganizationPhoneEntity(
            id="phone-2",
            phone_number="+7 098 765 4321"
        )
    ]


@pytest.fixture
def sample_organization_entity(
    sample_building_entity: BuildingEntity,
    sample_activity_entity: ActivityEntity,
    sample_phone_entities: List[OrganizationPhoneEntity]
) -> OrganizationEntity:
    """
    Фикстура для создания тестового OrganizationEntity с полными данными
    """
    return OrganizationEntity(
        id="org-1",
        title="Тестовый магазин",
        building_id="building-1",
        building=sample_building_entity,
        activities=[sample_activity_entity],
        phones=sample_phone_entities
    )


@pytest.fixture
def sample_organization_entity_minimal() -> OrganizationEntity:
    """
    Фикстура для создания минимального OrganizationEntity (без building, activities, phones)
    """
    return OrganizationEntity(
        id="org-2",
        title="Минимальная организация",
        building_id="building-2",
        building=None,
        activities=None,
        phones=None
    )


@pytest.fixture
def sample_organization_entities() -> List[OrganizationEntity]:
    """
    Фикстура для создания списка тестовых OrganizationEntity
    """
    return [
        OrganizationEntity(
            id="org-1",
            title="Магазин продуктов",
            building_id="building-1",
            building=None,
            activities=None,
            phones=None
        ),
        OrganizationEntity(
            id="org-2",
            title="Супермаркет",
            building_id="building-2",
            building=None,
            activities=None,
            phones=None
        ),
        OrganizationEntity(
            id="org-3",
            title="Кафе Москва",
            building_id="building-3",
            building=None,
            activities=None,
            phones=None
        )
    ]

