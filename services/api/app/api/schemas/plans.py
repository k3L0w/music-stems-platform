from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.enums import PlanCode


class PlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: PlanCode
    name: str
    monthly_price_brl: int | None
    active: bool
