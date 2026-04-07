from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.enums import PlanCode, SubscriptionStatus
from app.domain.models import Plan, Subscription


def list_plans(session: Session) -> list[Plan]:
    statement = select(Plan).order_by(Plan.name.asc())
    return list(session.scalars(statement))


def get_user_plan_code(session: Session, user_id: UUID) -> PlanCode:
    statement = (
        select(Plan.code)
        .join(Subscription, Subscription.plan_id == Plan.id)
        .where(Subscription.user_id == user_id)
        .where(Subscription.status == SubscriptionStatus.ACTIVE)
        .order_by(Subscription.started_at.desc().nullslast(), Subscription.id.desc())
        .limit(1)
    )
    plan_code = session.scalar(statement)
    return plan_code or PlanCode.FREE
