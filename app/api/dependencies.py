from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import async_session_maker
from app.repo.organization.repo import OrganizationRepo
from app.repo.building.repo import BuildingRepo
from app.usecase.organization.get_organization import GetOrganizationUseCase
from app.usecase.geo_search.search_use_case import GeoSearchUseCase


async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    """
    Dependency для проверки API ключа из заголовка X-API-Key
    """
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return x_api_key


async def get_db_session() -> AsyncSession:
    """
    Dependency для получения сессии БД
    """
    async with async_session_maker() as session:
        yield session


def get_organization_repo(session: AsyncSession = Depends(get_db_session)) -> OrganizationRepo:
    """
    Dependency для создания OrganizationRepo
    """
    return OrganizationRepo(session)


def get_building_repo(session: AsyncSession = Depends(get_db_session)) -> BuildingRepo:
    """
    Dependency для создания BuildingRepo
    """
    return BuildingRepo(session)


def get_organization_use_case(
    organization_repo: OrganizationRepo = Depends(get_organization_repo)
) -> GetOrganizationUseCase:
    """
    Dependency для создания GetOrganizationUseCase
    """
    return GetOrganizationUseCase(organization_repo)


def get_geo_search_use_case(
    organization_repo: OrganizationRepo = Depends(get_organization_repo),
    building_repo: BuildingRepo = Depends(get_building_repo)
) -> GeoSearchUseCase:
    """
    Dependency для создания GeoSearchUseCase
    """
    return GeoSearchUseCase(organization_repo, building_repo)

