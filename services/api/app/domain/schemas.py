from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UserRole(StrEnum):
    CUSTOMER = "customer"
    ADMIN = "admin"


class PlanCode(StrEnum):
    FREE = "free"
    SOLO = "solo"
    PRO = "pro"


class SubscriptionStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELED = "canceled"


class ProjectStatus(StrEnum):
    DRAFT = "draft"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingJobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class StemType(StrEnum):
    VOCALS = "vocals"
    DRUMS = "drums"
    BASS = "bass"
    GUITAR = "guitar"
    PIANO = "piano"
    OTHER = "other"


class UserSchema(BaseModel):
    id: UUID
    email: str
    display_name: str
    role: UserRole = UserRole.CUSTOMER
    created_at: datetime


class PlanSchema(BaseModel):
    id: UUID
    code: PlanCode
    name: str
    monthly_price_brl: Optional[int] = None
    active: bool = True


class SubscriptionSchema(BaseModel):
    id: UUID
    user_id: UUID
    plan_id: UUID
    status: SubscriptionStatus = SubscriptionStatus.PENDING
    started_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


class ProjectSchema(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    source_filename: str
    status: ProjectStatus = ProjectStatus.DRAFT
    created_at: datetime


class ProcessingJobSchema(BaseModel):
    id: UUID
    project_id: UUID
    status: ProcessingJobStatus = ProcessingJobStatus.QUEUED
    provider: str = "htdemucs_6s"
    requested_stems: list[StemType] = Field(default_factory=list)
    created_at: datetime


class GeneratedStemSchema(BaseModel):
    id: UUID
    project_id: UUID
    processing_job_id: UUID
    stem_type: StemType
    file_key: str
    created_at: datetime
