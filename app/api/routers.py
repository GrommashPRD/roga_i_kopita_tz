from fastapi import APIRouter
from app.api.handlers.organizations.organizations import router as organizations_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(organizations_router, prefix="/organizations", tags=["organizations"])

