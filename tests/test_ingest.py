from unittest.mock import AsyncMock, patch

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

URL = f"/ingest/{FAKE_EXP_ID}"
PUBLISH = "app.services.ingestion.mq.publish_ingest_message"


@pytest.mark.asyncio
async def test_ingest_404_unknown_experience():
    override_session_with(experience=None)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(f"/ingest/{UNKNOWN_ID}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_ingest_202_happy_path():
    session = override_session_with(
        experience=make_experience(), job=None
    )
    with patch(PUBLISH, new_callable=AsyncMock) as mock_pub:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            resp = await client.post(URL)

    assert resp.status_code == 202
    body = resp.json()
    assert body["status"] == "queued"
    assert body["id"] == str(FAKE_EXP_ID)
    mock_pub.assert_awaited_once_with(str(FAKE_EXP_ID))
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_ingest_409_already_queued():
    job = FakeJob(status=IngestionStatus.QUEUED)
    override_session_with(experience=make_experience(), job=job)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(URL)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_ingest_409_already_processing():
    job = FakeJob(status=IngestionStatus.PROCESSING)
    override_session_with(experience=make_experience(), job=job)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(URL)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_ingest_202_requeue_after_ingested():
    job = FakeJob(status=IngestionStatus.INGESTED)
    session = override_session_with(
        experience=make_experience(), job=job
    )
    with patch(PUBLISH, new_callable=AsyncMock):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            resp = await client.post(URL)

    assert resp.status_code == 202
    assert job.status == IngestionStatus.QUEUED
    assert job.error is None
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_ingest_202_requeue_after_failed():
    job = FakeJob(
        status=IngestionStatus.FAILED, error="previous error"
    )
    session = override_session_with(
        experience=make_experience(), job=job
    )
    with patch(PUBLISH, new_callable=AsyncMock):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            resp = await client.post(URL)

    assert resp.status_code == 202
    assert job.status == IngestionStatus.QUEUED
    assert job.error is None
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_ingest_503_publish_fails_rolls_back():
    session = override_session_with(
        experience=make_experience(), job=None
    )
    with patch(
        PUBLISH,
        new_callable=AsyncMock,
        side_effect=ConnectionError("rabbitmq down"),
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            resp = await client.post(URL)

    assert resp.status_code == 503
    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()
