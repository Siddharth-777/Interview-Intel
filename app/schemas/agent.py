from pydantic import BaseModel


class AgentRequest(BaseModel):
    question: str


class SourceCitation(BaseModel):
    experience_id: str
    company: str
    role: str
    round: str | None = None
    content_snippet: str


class AgentResponse(BaseModel):
    plan: str
    sources: list[SourceCitation]
