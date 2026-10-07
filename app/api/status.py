import uuid

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/status/{experience_id}")
async def get_status(experience_id: uuid.UUID) -> dict:
    # TODO: look up ingestion_jobs for this experience_id, return status
    raise HTTPException(status_code=501, detail="Not implemented")
