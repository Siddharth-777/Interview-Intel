from fastapi import FastAPI

from app.api import agent, health, ingest, status
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Interview Intel", version="0.1.0")

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(status.router)
app.include_router(agent.router)
