from pydantic import BaseModel


class RootResponse(BaseModel):
    name: str
    version: str
    environment: str
    docs_url: str


class HealthResponse(BaseModel):
    status: str
    service: str
