from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.enums import StemType


class StemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    processing_job_id: UUID
    stem_type: StemType
    file_key: str
    created_at: datetime


class StemDownloadTargetResponse(BaseModel):
    stem_id: UUID
    stem_type: StemType
    file_key: str
    download_url: str
    download_method: str
    expires_in_seconds: int
