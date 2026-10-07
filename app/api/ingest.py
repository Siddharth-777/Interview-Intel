import uuid

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/ingest/{experience_id}", status_code=202)
async def ingest_experience(experience_id: uuid.UUID) -> dict:
    # TODO: validate experience exists, create ingestion job, publish to RabbitMQ
    raise HTTPException(status_code=501, detail="Not implemented")
