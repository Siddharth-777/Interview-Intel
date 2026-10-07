from fastapi import APIRouter, HTTPException

from app.schemas.agent import AgentRequest

router = APIRouter()


@router.post("/agent")
async def ask_agent(request: AgentRequest) -> dict:
    # TODO: retrieve relevant chunks, generate 8-week plan via LLM
    raise HTTPException(status_code=501, detail="Not implemented")
