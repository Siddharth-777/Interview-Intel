import uuid

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import mq
from app.models.experience import InterviewExperience
from app.models.ingestion import IngestionJob, IngestionStatus


class ExperienceNotFoundError(Exception):
    pass


class AlreadyInProgressError(Exception):
    pass


class PublishFailedError(Exception):
    pass


async def start_ingestion(
    experience_id: uuid.UUID,
    session: AsyncSession,
) -> IngestionJob:
    result = await session.execute(
        select(InterviewExperience).where(
            InterviewExperience.id == experience_id
        )
    )
    if result.scalar_one_or_none() is None:
        raise ExperienceNotFoundError(experience_id)

    stmt = (
        pg_insert(IngestionJob)
        .values(experience_id=experience_id, status=IngestionStatus.QUEUED, error=None)
        .on_conflict_do_update(
            constraint="uq_ingestion_jobs_experience_id",
            set_={"status": IngestionStatus.QUEUED, "error": None},
            where=IngestionJob.status.in_(
                [IngestionStatus.INGESTED, IngestionStatus.FAILED]
            ),
        )
        .returning(IngestionJob)
    )

    try:
        result = await session.execute(stmt)
    except IntegrityError:
        await session.rollback()
        raise AlreadyInProgressError(experience_id)

    job = result.scalar_one_or_none()
    if job is None:
        await session.rollback()
        raise AlreadyInProgressError(experience_id)

    await session.flush()

    try:
        await mq.publish_ingest_message(str(experience_id))
    except Exception as exc:
        await session.rollback()
        raise PublishFailedError(str(exc)) from exc

    await session.commit()
    return job


async def get_ingestion_status(
    experience_id: uuid.UUID,
    session: AsyncSession,
) -> dict:
    result = await session.execute(
        select(InterviewExperience).where(
            InterviewExperience.id == experience_id
        )
    )
    if result.scalar_one_or_none() is None:
        raise ExperienceNotFoundError(experience_id)

    result = await session.execute(
        select(IngestionJob).where(
            IngestionJob.experience_id == experience_id
        )
    )
    job = result.scalar_one_or_none()

    if job is None:
        return {
            "experience_id": str(experience_id),
            "status": "waiting",
        }

    return {
        "experience_id": str(experience_id),
        "status": job.status.value,
        "error": job.error,
        "updated_at": job.updated_at,
    }
