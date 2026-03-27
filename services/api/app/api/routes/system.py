from fastapi import APIRouter

from app.api.schemas.system import HealthResponse, RootResponse
from app.core.settings import get_settings

router = APIRouter()


@router.get("/", response_model=RootResponse, tags=["system"])
def read_root() -> RootResponse:
    settings = get_settings()
    return RootResponse(
        name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
        docs_url=settings.docs_url,
    )


@router.get("/health", response_model=HealthResponse, tags=["system"])
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok", service="api")
