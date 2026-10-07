import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.ingestion import IngestionStatus
from tests.conftest import (
    FAKE_EXP_ID,
    UNKNOWN_ID,
    FakeJob,
    make_experience,
    override_session_with,
)


@pytest.mark.asyncio
async def test_status_404_unknown_experience():
    override_session_with(experience=None)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(f"/status/{UNKNOWN_ID}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_status_waiting_no_job():
    override_session_with(experience=make_experience(), job=None)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(f"/status/{FAKE_EXP_ID}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "waiting"
    assert body["experience_id"] == str(FAKE_EXP_ID)


@pytest.mark.asyncio
async def test_status_queued():
    job = FakeJob(status=IngestionStatus.QUEUED)
    override_session_with(experience=make_experience(), job=job)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(f"/status/{FAKE_EXP_ID}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "queued"
    assert body["error"] is None


@pytest.mark.asyncio
async def test_status_failed_with_error():
    job = FakeJob(
        status=IngestionStatus.FAILED,
        error="extraction timeout",
    )
    override_session_with(experience=make_experience(), job=job)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(f"/status/{FAKE_EXP_ID}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "failed"
    assert body["error"] == "extraction timeout"


@pytest.mark.asyncio
async def test_status_ingested():
    job = FakeJob(status=IngestionStatus.INGESTED)
    override_session_with(experience=make_experience(), job=job)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(f"/status/{FAKE_EXP_ID}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ingested"
