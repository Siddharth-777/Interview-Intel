import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.exc import IntegrityError

from app.core.db import get_session
from app.main import app
from tests.conftest import (
    FAKE_EXP_ID,
    UNKNOWN_ID,
    FakeJob,
    make_experience,
    mock_result,
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
        experience=make_experience(), job=FakeJob()
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
    override_session_with(experience=make_experience(), job=None)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(URL)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_ingest_409_already_processing():
    override_session_with(experience=make_experience(), job=None)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(URL)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_ingest_202_requeue_after_ingested():
    session = override_session_with(
        experience=make_experience(), job=FakeJob()
    )
    with patch(PUBLISH, new_callable=AsyncMock):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            resp = await client.post(URL)

    assert resp.status_code == 202
    assert resp.json()["status"] == "queued"
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_ingest_202_requeue_after_failed():
    session = override_session_with(
        experience=make_experience(), job=FakeJob()
    )
    with patch(PUBLISH, new_callable=AsyncMock):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            resp = await client.post(URL)

    assert resp.status_code == 202
    assert resp.json()["status"] == "queued"
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_ingest_503_publish_fails_rolls_back():
    session = override_session_with(
        experience=make_experience(), job=FakeJob()
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


@pytest.mark.asyncio
async def test_ingest_409_integrity_error():
    """IntegrityError from a DB race is mapped to 409."""
    session = AsyncMock()
    session.add = MagicMock()
    session.execute = AsyncMock(
        side_effect=[
            mock_result(make_experience()),
            IntegrityError("dup", {}, Exception()),
        ]
    )

    async def _dep():
        yield session

    app.dependency_overrides[get_session] = _dep

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(URL)
    assert resp.status_code == 409
    session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_ingest_concurrent_one_wins():
    """Two simultaneous POSTs → exactly one 202, one 409."""
    call_count = 0

    def _make_session():
        nonlocal call_count
        call_count += 1
        s = AsyncMock()
        s.add = MagicMock()
        if call_count == 1:
            s.execute = AsyncMock(
                side_effect=[
                    mock_result(make_experience()),
                    mock_result(FakeJob()),
                ]
            )
        else:
            s.execute = AsyncMock(
                side_effect=[
                    mock_result(make_experience()),
                    mock_result(None),
                ]
            )
        return s

    async def _dep():
        yield _make_session()

    app.dependency_overrides[get_session] = _dep

    with patch(PUBLISH, new_callable=AsyncMock) as mock_pub:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            r1, r2 = await asyncio.gather(
                client.post(URL),
                client.post(URL),
            )

    codes = sorted([r1.status_code, r2.status_code])
    assert codes == [202, 409]
    mock_pub.assert_awaited_once()
