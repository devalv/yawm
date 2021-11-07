# -*- coding: utf-8 -*-

import pytest

pytestmark = [pytest.mark.asyncio, pytest.mark.api_full]


async def test_health(backend_app):
    """Test that health checking handler working as expected."""
    resp = await backend_app.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"database": "online"}
