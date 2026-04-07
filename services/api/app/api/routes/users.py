from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.users import UserResponse
from app.db.dependencies import get_db_session
from app.db.repositories.plans import get_user_plan_code
from app.db.repositories.users import list_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def read_users(session: Session = Depends(get_db_session)) -> list[UserResponse]:
    users = list_users(session=session)
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            role=user.role,
            active_plan_code=get_user_plan_code(session=session, user_id=user.id),
        )
        for user in users
    ]
