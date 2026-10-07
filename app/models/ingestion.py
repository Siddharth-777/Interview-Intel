import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class IngestionStatus(enum.StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    INGESTED = "ingested"
    FAILED = "failed"


class IngestionJob(TimestampMixin, Base):
    __tablename__ = "ingestion_jobs"
    __table_args__ = (
        UniqueConstraint("experience_id", name="uq_ingestion_jobs_experience_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    experience_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interview_experiences.id"),
        nullable=False,
    )
    status: Mapped[IngestionStatus] = mapped_column(
        Enum(
            IngestionStatus,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
        default=IngestionStatus.QUEUED,
    )
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
