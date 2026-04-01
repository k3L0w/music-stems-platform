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
