import pytest
from app.api.schemas.mappers import (
    organization_entity_to_response,
    organization_entity_to_simple_response,
    organization_entity_to_with_building_response,
    building_entity_to_response
)
from app.api.schemas.organization import (
    OrganizationResponse,
    OrganizationSimpleResponse,
    OrganizationWithBuildingResponse
)
from app.api.schemas.building import BuildingResponse


class TestOrganizationEntityToResponse:
    """Тесты для organization_entity_to_response"""
    
    def test_full_organization_mapping(self, sample_organization_entity):
        """Тест преобразования полной организации"""
        result = organization_entity_to_response(sample_organization_entity)
        
        assert isinstance(result, OrganizationResponse)
        assert result.id == "org-1"
        assert result.title == "Тестовый магазин"
        assert result.building_id == "building-1"
        assert result.building is not None
        assert result.building.id == "building-1"
        assert result.building.address == "Москва, ул. Тестовая, д. 1"
        assert len(result.activities) == 1
        assert result.activities[0].name == "Розничная торговля"
        assert len(result.phones) == 2
        assert result.phones[0].phone_number == "+7 123 456 7890"
    
    def test_minimal_organization_mapping(self, sample_organization_entity_minimal):
        """Тест преобразования минимальной организации"""
        result = organization_entity_to_response(sample_organization_entity_minimal)
        
        assert isinstance(result, OrganizationResponse)
        assert result.id == "org-2"
        assert result.title == "Минимальная организация"
        assert result.building is None
        assert result.activities is None
        assert result.phones is None


class TestOrganizationEntityToSimpleResponse:
    """Тесты для organization_entity_to_simple_response"""
    
    def test_simple_response_with_phones(self, sample_organization_entity):
        """Тест преобразования в упрощенный ответ с телефонами"""
        result = organization_entity_to_simple_response(sample_organization_entity)
        
        assert isinstance(result, OrganizationSimpleResponse)
        assert result.title == "Тестовый магазин"
        assert len(result.phones) == 2
        assert "+7 123 456 7890" in result.phones
        assert "+7 098 765 4321" in result.phones
    
    def test_simple_response_without_phones(self, sample_organization_entity_minimal):
        """Тест преобразования в упрощенный ответ без телефонов"""
        result = organization_entity_to_simple_response(sample_organization_entity_minimal)
        
        assert isinstance(result, OrganizationSimpleResponse)
        assert result.title == "Минимальная организация"
        assert result.phones == []


class TestOrganizationEntityToWithBuildingResponse:
    """Тесты для organization_entity_to_with_building_response"""
    
    def test_with_building_response_full(self, sample_organization_entity):
        """Тест преобразования с зданием и телефонами"""
        result = organization_entity_to_with_building_response(sample_organization_entity)
        
        assert isinstance(result, OrganizationWithBuildingResponse)
        assert result.title == "Тестовый магазин"
        assert len(result.phones) == 2
        assert result.building is not None
        assert result.building.id == "building-1"
        assert result.building.address == "Москва, ул. Тестовая, д. 1"
        assert result.building.latitude == 55.7558
        assert result.building.longitude == 37.6173
    
    def test_with_building_response_no_building(self, sample_organization_entity_minimal):
        """Тест преобразования без здания"""
        result = organization_entity_to_with_building_response(sample_organization_entity_minimal)
        
        assert isinstance(result, OrganizationWithBuildingResponse)
        assert result.title == "Минимальная организация"
        assert result.phones == []
        assert result.building is None


class TestBuildingEntityToResponse:
    """Тесты для building_entity_to_response"""
    
    def test_building_mapping(self, sample_building_entity):
        """Тест преобразования здания"""
        result = building_entity_to_response(sample_building_entity)
        
        assert isinstance(result, BuildingResponse)
        assert result.id == "building-1"
        assert result.address == "Москва, ул. Тестовая, д. 1"
        assert result.latitude == 55.7558
        assert result.longitude == 37.6173

