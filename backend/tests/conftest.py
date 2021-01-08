# -*- coding: utf-8 -*-
"""Common project fixtures."""

from api import app

from async_asgi_testclient import TestClient

import pytest


@pytest.fixture()
async def api_client():
    """Fixture for async api http tests.

    Each test take new client.
    """
    async with TestClient(app) as client:
        yield client
