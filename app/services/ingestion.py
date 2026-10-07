import uuid

from sqlalchemy import select
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

    result = await session.execute(
        select(IngestionJob).where(
            IngestionJob.experience_id == experience_id
        )
    )
    job = result.scalar_one_or_none()

    if job is not None and job.status in (
        IngestionStatus.QUEUED,
        IngestionStatus.PROCESSING,
    ):
        raise AlreadyInProgressError(experience_id)

    if job is not None:
        job.status = IngestionStatus.QUEUED
        job.error = None
    else:
        job = IngestionJob(experience_id=experience_id)
        session.add(job)

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
