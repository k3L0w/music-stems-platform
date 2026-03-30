from fastapi import APIRouter

from app.api.routes.jobs import router as jobs_router
from app.api.routes.plans import router as plans_router
from app.api.routes.projects import router as projects_router
from app.api.routes.system import router as system_router

api_router = APIRouter()
api_router.include_router(system_router)
api_router.include_router(plans_router)
api_router.include_router(projects_router)
api_router.include_router(jobs_router)
