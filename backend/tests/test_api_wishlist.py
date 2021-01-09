# -*- coding: utf-8 -*-
"""Wishlist api tests."""

import pytest


pytestmark = [pytest.mark.asyncio]

# TODO: empty database for each test?

# TODO: создание продукта
# TODO: редактирование продукта
# TODO: удаление продукта
# TODO: просмотр продукта
#
# TODO: создание вишлиста
# TODO: удаление вишлиста без продуктов
# TODO: редактирование вишлиста
# TODO: просмотр вишлиста
# tODO: добавление продукта в вишлист
# TODO: удаление продукта из вишлиста
# TODO: резервирование продукта в вишлисте
#
# TODO: удаление вишлиста с продуктами
# TODO: удаление продукта находящегося в вишлистах
# TODO: просмотр продуктов в вишлисте


async def test_trailing_slash(api_client):
    """Test that trailing slash redirects working."""
    resp = await api_client.get("/api/products/")
    assert resp.is_redirect
    assert resp.status_code == 307


class TestProduct:
    """Product API tests."""

    API_URL = "/api/products"

    async def test_product_create(self, snapshot, api_client):
        """Product CREATE operation test."""
        resp = await api_client.post(
            self.API_URL,
            json={"name": "Product1", "url": "product1", "price": "123.99"},
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    async def test_products(self, api_client):
        """Product LIST operation test."""
        resp = await api_client.get(self.API_URL)
        assert resp.status_code == 200
        # TODO: assert json
