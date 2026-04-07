from uuid import UUID

from pydantic import BaseModel

from app.domain.enums import PlanCode, UserRole


class UserResponse(BaseModel):
    id: UUID
    email: str
    display_name: str
    role: UserRole
    active_plan_code: PlanCode
