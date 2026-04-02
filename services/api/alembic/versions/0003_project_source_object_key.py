"""add project source object key

Revision ID: 0003_project_source_object_key
Revises: 0002_project_upload_metadata
Create Date: 2026-04-02 00:00:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0003_project_source_object_key"
down_revision: str | None = "0002_project_upload_metadata"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("source_object_key", sa.String(length=512), nullable=True))


def downgrade() -> None:
    op.drop_column("projects", "source_object_key")
