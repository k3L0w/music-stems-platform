from uuid import UUID

from pydantic import BaseModel, Field


class UploadTargetResponse(BaseModel):
    project_id: UUID
    object_key: str
    upload_url: str
    upload_method: str
    upload_headers: dict[str, str]
    expires_in_seconds: int


class UploadCompleteRequest(BaseModel):
    object_key: str = Field(min_length=1, max_length=512)
    source_filename: str | None = Field(default=None, min_length=1, max_length=255)
    source_content_type: str | None = Field(default=None, min_length=1, max_length=255)
    source_size_bytes: int | None = Field(default=None, ge=0)
