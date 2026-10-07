import uuid
from datetime import datetime

from pydantic import BaseModel


class IngestResponse(BaseModel):
    id: uuid.UUID
    status: str


class IngestionJobOut(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    experience_id: uuid.UUID
    status: str
    error: str | None = None
    created_at: datetime
    updated_at: datetime
