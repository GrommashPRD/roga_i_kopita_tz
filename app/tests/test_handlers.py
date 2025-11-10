import pytest
from unittest.mock import AsyncMock, MagicMock, patch, MagicMock as MockModule
from fastapi import HTTPException
from fastapi.testclient import TestClient

# Мокируем geoalchemy2 до импорта app, чтобы избежать ошибок импорта
try:
    import geoalchemy2
except ImportError:
    import sys
    # Создаем мок-модуль для geoalchemy2
    geoalchemy2_mock = MockModule()
    geoalchemy2_mock.functions = MockModule()
    geoalchemy2_mock.types = MockModule()
    sys.modules['geoalchemy2'] = geoalchemy2_mock
    sys.modules['geoalchemy2.functions'] = geoalchemy2_mock.functions
    sys.modules['geoalchemy2.types'] = geoalchemy2_mock.types

# Теперь можно безопасно импортировать app
from app.main import app
from app.api.dependencies import get_organization_use_case, get_geo_search_use_case, verify_api_key
from app.usecase.organization.get_organization import GetOrganizationUseCase
from app.usecase.geo_search.search_use_case import GeoSearchUseCase
from app.exceptions import NotFoundError, UseCaseExecutionError, DatabaseError


# Мокируем verify_api_key для всех тестов handlers
@pytest.fixture(autouse=True)
def mock_verify_api_key():
    """Автоматически мокирует verify_api_key для всех тестов handlers"""
    # Мок всегда возвращает валидный ключ
    async def verify_mock(x_api_key: str = None):
        return x_api_key or "test-api-key"
    
    # Используем dependency_overrides для переопределения verify_api_key
    app.dependency_overrides[verify_api_key] = verify_mock
    yield
    app.dependency_overrides.pop(verify_api_key, None)


class TestGetOrganizationsByBuilding:
    """Тесты для handler get_organizations_by_building"""
    
    @pytest.fixture
    def mock_use_case(self):
        """Фикстура для мок UseCase"""
        return MagicMock(spec=GetOrganizationUseCase)
    
    @pytest.fixture
    def client(self, mock_use_case):
        """Фикстура для тестового клиента с мок UseCase"""
        app.dependency_overrides[get_organization_use_case] = lambda: mock_use_case
        yield TestClient(app)
        app.dependency_overrides.clear()
    
    def test_success(self, client, mock_use_case, sample_organization_entities):
        """Тест успешного получения организаций по building_id"""
        mock_use_case.list_by_building = AsyncMock(return_value=sample_organization_entities[:2])
        
        response = client.get(
            "/api/v1/organizations/by-building/building-1",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Магазин продуктов"
        assert data[1]["title"] == "Супермаркет"
    
    def test_not_found(self, client, mock_use_case):
        """Тест случая, когда организации не найдены"""
        mock_use_case.list_by_building = AsyncMock(side_effect=NotFoundError("Organizations for building building-999 not found"))
        
        response = client.get(
            "/api/v1/organizations/by-building/building-999",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_internal_error(self, client, mock_use_case):
        """Тест случая внутренней ошибки сервера"""
        mock_use_case.list_by_building = AsyncMock(side_effect=UseCaseExecutionError("Internal error"))
        
        response = client.get(
            "/api/v1/organizations/by-building/building-1",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal server error"


class TestGetOrganizationsByActivityExact:
    """Тесты для handler get_organizations_by_activity_exact"""
    
    @pytest.fixture
    def mock_use_case(self):
        return MagicMock(spec=GetOrganizationUseCase)
    
    @pytest.fixture
    def client(self, mock_use_case):
        app.dependency_overrides[get_organization_use_case] = lambda: mock_use_case
        yield TestClient(app)
        app.dependency_overrides.clear()
    
    def test_success(self, client, mock_use_case, sample_organization_entities):
        """Тест успешного получения организаций по виду деятельности"""
        mock_use_case.list_by_activity_exact = AsyncMock(return_value=sample_organization_entities[:1])
        
        response = client.get(
            "/api/v1/organizations/by-activity/exact?activity_name=Розничная торговля",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Магазин продуктов"


class TestGetOrgByName:
    """Тесты для handler get_org_by_name"""
    
    @pytest.fixture
    def mock_use_case(self):
        return MagicMock(spec=GetOrganizationUseCase)
    
    @pytest.fixture
    def client(self, mock_use_case):
        app.dependency_overrides[get_organization_use_case] = lambda: mock_use_case
        yield TestClient(app)
        app.dependency_overrides.clear()
    
    def test_success_partial_match(self, client, mock_use_case, sample_organization_entities):
        """Тест успешного поиска по частичному совпадению названия"""
        mock_use_case.get_by_name = AsyncMock(return_value=sample_organization_entities[:2])
        
        response = client.get(
            "/api/v1/organizations/by-name?organization_name=магазин",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(org["title"] == "Магазин продуктов" for org in data)
        assert any(org["title"] == "Супермаркет" for org in data)
    
    def test_not_found(self, client, mock_use_case):
        """Тест случая, когда организации не найдены"""
        mock_use_case.get_by_name = AsyncMock(side_effect=NotFoundError("Organizations with name containing 'несуществующая' not found"))
        
        response = client.get(
            "/api/v1/organizations/by-name?organization_name=несуществующая",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 404


class TestGetOrgById:
    """Тесты для handler get_org_by_id"""
    
    @pytest.fixture
    def mock_use_case(self):
        return MagicMock(spec=GetOrganizationUseCase)
    
    @pytest.fixture
    def client(self, mock_use_case):
        app.dependency_overrides[get_organization_use_case] = lambda: mock_use_case
        yield TestClient(app)
        app.dependency_overrides.clear()
    
    def test_success(self, client, mock_use_case, sample_organization_entity):
        """Тест успешного получения организации по ID"""
        mock_use_case.get_by_id = AsyncMock(return_value=sample_organization_entity)
        
        response = client.get(
            "/api/v1/organizations/org-1",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "org-1"
        assert data["title"] == "Тестовый магазин"
    
    def test_not_found(self, client, mock_use_case):
        """Тест случая, когда организация не найдена"""
        mock_use_case.get_by_id = AsyncMock(side_effect=NotFoundError("Organization with id org-999 not found"))
        
        response = client.get(
            "/api/v1/organizations/org-999",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 404
    
    def test_internal_error(self, client, mock_use_case):
        """Тест случая внутренней ошибки сервера"""
        mock_use_case.get_by_id = AsyncMock(side_effect=UseCaseExecutionError("Internal error"))
        
        response = client.get(
            "/api/v1/organizations/org-1",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal server error"


class TestSearchByRadius:
    """Тесты для handler search_by_radius"""
    
    @pytest.fixture
    def mock_use_case(self):
        return MagicMock(spec=GeoSearchUseCase)
    
    @pytest.fixture
    def client(self, mock_use_case):
        app.dependency_overrides[get_geo_search_use_case] = lambda: mock_use_case
        yield TestClient(app)
        app.dependency_overrides.clear()
    
    def test_success(self, client, mock_use_case, sample_organization_entities):
        """Тест успешного поиска по радиусу"""
        mock_use_case.search_by_radius = AsyncMock(return_value=(sample_organization_entities[:2], []))
        
        response = client.get(
            "/api/v1/organizations/search/radius?latitude=55.7558&longitude=37.6173&radius_meters=1000",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "organizations" in data
        assert len(data["organizations"]) == 2
    
    def test_internal_error(self, client, mock_use_case):
        """Тест случая внутренней ошибки сервера"""
        mock_use_case.search_by_radius = AsyncMock(side_effect=UseCaseExecutionError("Internal error"))
        
        response = client.get(
            "/api/v1/organizations/search/radius?latitude=55.7558&longitude=37.6173&radius_meters=1000",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal server error"


class TestSearchByRectangle:
    """Тесты для handler search_by_rectangle"""
    
    @pytest.fixture
    def mock_use_case(self):
        return MagicMock(spec=GeoSearchUseCase)
    
    @pytest.fixture
    def client(self, mock_use_case):
        app.dependency_overrides[get_geo_search_use_case] = lambda: mock_use_case
        yield TestClient(app)
        app.dependency_overrides.clear()
    
    def test_success(self, client, mock_use_case, sample_organization_entities):
        """Тест успешного поиска по прямоугольной области"""
        mock_use_case.search_by_rectangle = AsyncMock(return_value=(sample_organization_entities[:1], []))
        
        response = client.get(
            "/api/v1/organizations/search/rectangle?min_latitude=55.0&min_longitude=37.0&max_latitude=56.0&max_longitude=38.0",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "organizations" in data
        assert len(data["organizations"]) == 1
    
    def test_internal_error(self, client, mock_use_case):
        """Тест случая внутренней ошибки сервера"""
        mock_use_case.search_by_rectangle = AsyncMock(side_effect=UseCaseExecutionError("Internal error"))
        
        response = client.get(
            "/api/v1/organizations/search/rectangle?min_latitude=55.0&min_longitude=37.0&max_latitude=56.0&max_longitude=38.0",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal server error"

