from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import (
    PlanCode,
    ProcessingJobStatus,
    ProjectStatus,
    StemType,
    SubscriptionStatus,
    UserRole,
)


class DomainSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserSchema(DomainSchema):
    id: UUID
    email: str
    display_name: str
    role: UserRole = UserRole.CUSTOMER
    created_at: datetime


class PlanSchema(DomainSchema):
    id: UUID
    code: PlanCode
    name: str
    monthly_price_brl: Optional[int] = None
    active: bool = True


class SubscriptionSchema(DomainSchema):
    id: UUID
    user_id: UUID
    plan_id: UUID
    status: SubscriptionStatus = SubscriptionStatus.PENDING
    started_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


class ProjectSchema(DomainSchema):
    id: UUID
    user_id: UUID
    name: str
    source_filename: str
    source_content_type: Optional[str] = None
    source_size_bytes: Optional[int] = None
    status: ProjectStatus = ProjectStatus.DRAFT
    created_at: datetime


class ProcessingJobSchema(DomainSchema):
    id: UUID
    project_id: UUID
    status: ProcessingJobStatus = ProcessingJobStatus.QUEUED
    provider: str = "htdemucs_6s"
    requested_stems: list[StemType] = Field(default_factory=list)
    created_at: datetime


class GeneratedStemSchema(DomainSchema):
    id: UUID
    project_id: UUID
    processing_job_id: UUID
    stem_type: StemType
    file_key: str
    created_at: datetime
