# -*- coding: utf-8 -*-
"""Common project fixtures."""

from api import app

from async_asgi_testclient import TestClient

import pytest


@pytest.fixture()
def _run_migrations(alembic_runner):
    """Upgrade database to a latest alembic migration."""
    alembic_runner.managed_upgrade("head")


@pytest.fixture()
async def api_client(_run_migrations):
    """Fixture for async api http tests.

    Each test take new client.
    """
    async with TestClient(app) as client:
        yield client
