# -*- coding: utf-8 -*-
"""Wishlist api tests."""

from async_asgi_testclient import TestClient

import pytest

# TODO: test for trailing slash
# TODO: test database for READ operations
# TODO:


@pytest.mark.asyncio
async def test_wishlist_app():
    """Wishlist app tests."""
    from api import app

    async with TestClient(app) as client:
        resp = await client.get("/api/wishlists")
        print(resp)
        print(resp.json())
        # assert resp.status_code == 200
        # assert resp.text == "plain response"

        # resp = await client.get("/json")
        # assert resp.status_code == 200
        # assert resp.json() == {"hello": "world"}
