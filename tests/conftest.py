import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.db import get_session
from app.main import app
from app.models.ingestion import IngestionStatus

FAKE_EXP_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
UNKNOWN_ID = uuid.UUID("00000000-0000-0000-0000-ffffffffffff")


def mock_result(value):
    """Wrap a value so result.scalar_one_or_none() returns it."""
    r = MagicMock()
    r.scalar_one_or_none.return_value = value
    return r


def make_experience():
    exp = MagicMock()
    exp.id = FAKE_EXP_ID
    return exp


class FakeJob:
    def __init__(
        self,
        experience_id=FAKE_EXP_ID,
        status=IngestionStatus.QUEUED,
        error=None,
    ):
        self.id = uuid.uuid4()
        self.experience_id = experience_id
        self.status = status
        self.error = error
        self.updated_at = datetime.now(UTC)
        self.created_at = datetime.now(UTC)

    @property
    def value(self):
        return self.status.value


def override_session_with(experience=None, job=None):
    """Override get_session; returns the mock session for assertions."""
    session = AsyncMock()
    session.add = MagicMock()
    session.execute = AsyncMock(
        side_effect=[
            mock_result(experience),
            mock_result(job),
        ]
    )

    async def _dep():
        yield session

    app.dependency_overrides[get_session] = _dep
    return session


@pytest.fixture(autouse=True)
def _clear_overrides():
    yield
    app.dependency_overrides.clear()
