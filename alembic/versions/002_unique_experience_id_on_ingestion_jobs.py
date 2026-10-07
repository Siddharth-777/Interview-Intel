"""add unique constraint on ingestion_jobs.experience_id

Revision ID: 002
Revises: 001
Create Date: 2026-10-07
"""
from collections.abc import Sequence

from alembic import op

revision: str = "002"
down_revision: str = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_ingestion_jobs_experience_id",
        "ingestion_jobs",
        ["experience_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_ingestion_jobs_experience_id",
        "ingestion_jobs",
        type_="unique",
    )
