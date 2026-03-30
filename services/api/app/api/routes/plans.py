from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.plans import PlanResponse
from app.db.dependencies import get_db_session
from app.db.repositories.plans import list_plans

router = APIRouter(prefix="/plans", tags=["plans"])


@router.get("", response_model=list[PlanResponse])
def read_plans(session: Session = Depends(get_db_session)) -> list[PlanResponse]:
    plans = list_plans(session)
    return [PlanResponse.model_validate(plan) for plan in plans]
