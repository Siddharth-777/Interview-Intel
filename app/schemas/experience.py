import uuid
from datetime import datetime

from pydantic import BaseModel


class InterviewExperienceOut(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    company: str
    role: str
    year: int
    raw_text: str
    created_at: datetime
