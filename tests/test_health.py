import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health_returns_ok():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_ingest_returns_501():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/ingest/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 501


@pytest.mark.asyncio
async def test_status_returns_501():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/status/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 501


@pytest.mark.asyncio
async def test_agent_returns_501():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/agent", json={"question": "test"})
    assert response.status_code == 501
