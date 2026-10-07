import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.status import StatusResponse
from app.services.ingestion import (
    ExperienceNotFoundError,
    get_ingestion_status,
)

router = APIRouter()


@router.get(
    "/status/{experience_id}",
    response_model=StatusResponse,
)
async def get_status(
    experience_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> StatusResponse:
    try:
        result = await get_ingestion_status(
            experience_id, session
        )
    except ExperienceNotFoundError:
        raise HTTPException(404, "Experience not found")
    return StatusResponse(**result)
