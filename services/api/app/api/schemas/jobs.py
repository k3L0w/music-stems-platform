from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import ProcessingJobStatus, StemType


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    provider: str
    requested_stems: list[StemType]
    status: ProcessingJobStatus
    created_at: datetime


class JobCreateRequest(BaseModel):
    provider: str = Field(default="htdemucs_6s", min_length=1, max_length=120)
    requested_stems: list[StemType] = Field(min_length=1)
