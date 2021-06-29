# -*- coding: utf-8 -*-
"""Common project fixtures."""

import pytest
from async_asgi_testclient import TestClient

from ..api import app


@pytest.fixture
def alembic_config():
    return {"script_location": "core/database/migrations"}


@pytest.fixture
async def api_client(alembic_runner):
    """Fixture for async api http tests.

    Each test take new client.
    """
    # upgrade database to a latest alembic migration.
    alembic_runner.managed_upgrade("head")

    async with TestClient(app) as client:
        yield client

    # clear all data in database by downgrade alembic migrations.
    alembic_runner.migrate_down_to("base")


def pytest_sessionfinish(session, exitstatus):
    """Disable exit code 5 if no tests found."""
    if exitstatus == 5:
        session.exitstatus = 0
