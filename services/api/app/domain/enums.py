from enum import StrEnum


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
