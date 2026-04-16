"""add processing job timestamps

Revision ID: 0004_processing_job_timestamps
Revises: 0003_project_source_object_key
Create Date: 2026-04-08 00:00:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0004_processing_job_timestamps"
down_revision: str | None = "0003_project_source_object_key"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("processing_jobs", sa.Column("started_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("processing_jobs", sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("processing_jobs", "finished_at")
    op.drop_column("processing_jobs", "started_at")
