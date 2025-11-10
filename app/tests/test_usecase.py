import pytest
from unittest.mock import AsyncMock, MagicMock
from app.usecase.organization.get_organization import GetOrganizationUseCase
from app.entity.organization import OrganizationEntity
from app.exceptions import NotFoundError, UseCaseExecutionError, DatabaseError


class TestGetOrganizationUseCase:
    """Тесты для GetOrganizationUseCase"""
    
    @pytest.fixture
    def mock_repo(self):
        """Фикстура для мок-репозитория"""
        return MagicMock()
    
    @pytest.fixture
    def use_case(self, mock_repo):
        """Фикстура для создания UseCase с мок-репозиторием"""
        return GetOrganizationUseCase(mock_repo)
    
    @pytest.mark.asyncio
    async def test_get_by_id_success(self, use_case, mock_repo, sample_organization_entity):
        """Тест успешного получения организации по ID"""
        mock_repo.get_org_by_id = AsyncMock(return_value=sample_organization_entity)
        
        result = await use_case.get_by_id("org-1")
        
        assert result == sample_organization_entity
        mock_repo.get_org_by_id.assert_called_once_with("org-1")
    
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, use_case, mock_repo):
        """Тест получения организации по ID, когда она не найдена"""
        mock_repo.get_org_by_id = AsyncMock(return_value=None)
        
        with pytest.raises(NotFoundError, match="Organization with id org-999 not found"):
            await use_case.get_by_id("org-999")
        
        mock_repo.get_org_by_id.assert_called_once_with("org-999")
    
    @pytest.mark.asyncio
    async def test_get_by_id_database_error(self, use_case, mock_repo):
        """Тест получения организации по ID при ошибке БД"""
        mock_repo.get_org_by_id = AsyncMock(side_effect=DatabaseError("Database connection error"))
        
        with pytest.raises(UseCaseExecutionError):
            await use_case.get_by_id("org-1")
        
        mock_repo.get_org_by_id.assert_called_once_with("org-1")
    
    @pytest.mark.asyncio
    async def test_get_by_name_success(self, use_case, mock_repo, sample_organization_entities):
        """Тест успешного получения организаций по частичному совпадению названия"""
        mock_repo.get_org_by_name = AsyncMock(return_value=sample_organization_entities[:2])
        
        result = await use_case.get_by_name("магазин")
        
        assert len(result) == 2
        assert result[0].title == "Магазин продуктов"
        assert result[1].title == "Супермаркет"
        mock_repo.get_org_by_name.assert_called_once_with("магазин")
    
    @pytest.mark.asyncio
    async def test_get_by_name_not_found(self, use_case, mock_repo):
        """Тест получения организаций по названию, когда они не найдены"""
        mock_repo.get_org_by_name = AsyncMock(return_value=[])
        
        with pytest.raises(NotFoundError, match="Organizations with name containing несуществующая not found"):
            await use_case.get_by_name("несуществующая")
        
        mock_repo.get_org_by_name.assert_called_once_with("несуществующая")
    
    @pytest.mark.asyncio
    async def test_list_by_building_success(self, use_case, mock_repo, sample_organization_entities):
        """Тест успешного получения списка организаций по building_id"""
        mock_repo.list_by_building = AsyncMock(return_value=sample_organization_entities)
        
        result = await use_case.list_by_building("building-1")
        
        assert len(result) == 3
        mock_repo.list_by_building.assert_called_once_with("building-1")
    
    @pytest.mark.asyncio
    async def test_list_by_building_not_found(self, use_case, mock_repo):
        """Тест получения списка организаций по building_id, когда они не найдены"""
        mock_repo.list_by_building = AsyncMock(return_value=[])
        
        with pytest.raises(NotFoundError, match="Organizations for building building-999 not found"):
            await use_case.list_by_building("building-999")
        
        mock_repo.list_by_building.assert_called_once_with("building-999")
    
    @pytest.mark.asyncio
    async def test_list_by_activity_exact_success(self, use_case, mock_repo, sample_organization_entities):
        """Тест успешного получения списка организаций по виду деятельности"""
        mock_repo.list_by_activity_exact = AsyncMock(return_value=sample_organization_entities[:1])
        
        result = await use_case.list_by_activity_exact("Розничная торговля")
        
        assert len(result) == 1
        mock_repo.list_by_activity_exact.assert_called_once_with("Розничная торговля")
    
    @pytest.mark.asyncio
    async def test_list_by_activity_exact_not_found(self, use_case, mock_repo):
        """Тест получения списка организаций по виду деятельности, когда они не найдены"""
        mock_repo.list_by_activity_exact = AsyncMock(return_value=[])
        
        with pytest.raises(NotFoundError, match="Organizations for activity Несуществующая деятельность not found"):
            await use_case.list_by_activity_exact("Несуществующая деятельность")
        
        mock_repo.list_by_activity_exact.assert_called_once_with("Несуществующая деятельность")
    
    @pytest.mark.asyncio
    async def test_list_by_activity_tree_success(self, use_case, mock_repo, sample_organization_entities):
        """Тест успешного получения списка организаций по виду деятельности с иерархией"""
        mock_repo.list_by_activity_hierarchy = AsyncMock(return_value=sample_organization_entities)
        
        result = await use_case.list_by_activity_tree("Розничная торговля")
        
        assert len(result) == 3
        mock_repo.list_by_activity_hierarchy.assert_called_once_with("Розничная торговля")
    
    @pytest.mark.asyncio
    async def test_list_by_activity_tree_not_found(self, use_case, mock_repo):
        """Тест получения списка организаций по виду деятельности с иерархией, когда они не найдены"""
        mock_repo.list_by_activity_hierarchy = AsyncMock(return_value=[])
        
        with pytest.raises(NotFoundError, match="Organizations for activity Несуществующая деятельность not found"):
            await use_case.list_by_activity_tree("Несуществующая деятельность")
        
        mock_repo.list_by_activity_hierarchy.assert_called_once_with("Несуществующая деятельность")

