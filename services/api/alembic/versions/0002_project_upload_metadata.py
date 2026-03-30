"""add project upload metadata columns

Revision ID: 0002_project_upload_metadata
Revises: 0001_initial_schema
Create Date: 2026-03-30 00:00:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0002_project_upload_metadata"
down_revision: str | None = "0001_initial_schema"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("source_content_type", sa.String(length=255), nullable=True))
    op.add_column("projects", sa.Column("source_size_bytes", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("projects", "source_size_bytes")
    op.drop_column("projects", "source_content_type")
