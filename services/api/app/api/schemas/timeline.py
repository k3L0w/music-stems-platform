from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProjectTimelineEventResponse(BaseModel):
    type: str
    timestamp: datetime
    title: str
    description: str
    job_id: UUID | None = None
    stem_id: UUID | None = None
