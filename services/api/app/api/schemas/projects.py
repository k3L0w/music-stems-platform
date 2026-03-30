from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import ProjectStatus


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    name: str
    source_filename: str
    source_content_type: str | None
    source_size_bytes: int | None
    status: ProjectStatus
    created_at: datetime


class ProjectCreateRequest(BaseModel):
    user_id: UUID
    name: str = Field(min_length=1, max_length=255)
    source_filename: str = Field(min_length=1, max_length=255)
    source_content_type: str | None = Field(default=None, min_length=1, max_length=255)
    source_size_bytes: int | None = Field(default=None, ge=0)
    status: ProjectStatus = ProjectStatus.DRAFT


class ProjectUpdateRequest(BaseModel):
    user_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    source_filename: str | None = Field(default=None, min_length=1, max_length=255)
    source_content_type: str | None = Field(default=None, min_length=1, max_length=255)
    source_size_bytes: int | None = Field(default=None, ge=0)
    status: ProjectStatus | None = None
