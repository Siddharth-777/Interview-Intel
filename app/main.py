from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import agent, health, ingest, status
from app.core import mq
from app.core.logging import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await mq.close_connection()


app = FastAPI(
    title="Interview Intel", version="0.1.0", lifespan=lifespan
)

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(status.router)
app.include_router(agent.router)
