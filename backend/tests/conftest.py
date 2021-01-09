# -*- coding: utf-8 -*-
"""Common project fixtures."""

from api import app

from async_asgi_testclient import TestClient

import pytest


@pytest.fixture()
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
