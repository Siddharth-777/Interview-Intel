from datetime import datetime

from pydantic import BaseModel


class StatusResponse(BaseModel):
    experience_id: str
    status: str
    error: str | None = None
    updated_at: datetime | None = None
