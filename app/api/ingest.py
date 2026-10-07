import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.ingestion import IngestResponse
from app.services.ingestion import (
    AlreadyInProgressError,
    ExperienceNotFoundError,
    PublishFailedError,
    start_ingestion,
)

router = APIRouter()


@router.post(
    "/ingest/{experience_id}",
    status_code=202,
    response_model=IngestResponse,
)
async def ingest_experience(
    experience_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> IngestResponse:
    try:
        await start_ingestion(experience_id, session)
    except ExperienceNotFoundError:
        raise HTTPException(404, "Experience not found")
    except AlreadyInProgressError:
        raise HTTPException(
            409, "Ingestion already queued or in progress"
        )
    except PublishFailedError:
        raise HTTPException(
            503, "Failed to publish to message queue"
        )
    return IngestResponse(id=experience_id, status="queued")
