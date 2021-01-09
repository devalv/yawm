# -*- coding: utf-8 -*-
"""Wishlist api tests."""
from api.models.wishlist import Product

import pytest

pytestmark = [pytest.mark.asyncio]

# TODO: empty database for each test?

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


@pytest.fixture()
async def _nine_products():
    for i in range(1, 10):
        await Product.create(name=f"test{i}", url=f"test-url{i}", price=f"12{i}.3{i}")


@pytest.fixture()
async def one_product():
    product = await Product.create(name="test", url="test-url", price="12.3")
    return product


async def test_trailing_slash(api_client):
    """Test that trailing slash redirects working."""
    resp = await api_client.get("/api/products/")
    assert resp.is_redirect
    assert resp.status_code == 307


class TestProduct:
    """Product API tests."""

    API_URL = "/api/products"

    async def test_product_create(self, snapshot, api_client):
        resp = await api_client.post(
            self.API_URL,
            json={"name": "Product1", "url": "product1", "price": "123.99"},
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    async def test_products(self, snapshot, api_client, _nine_products):
        resp = await api_client.get(self.API_URL)
        assert resp.status_code == 200
        resp_data = resp.json()
        for resp_product in resp_data:
            resp_product.pop("uid", None)
        snapshot.assert_match(resp_data)

    async def test_product_read(self, snapshot, api_client, one_product):
        resp = await api_client.get(self.API_URL + f"/{one_product.uid}")
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    async def test_product_delete(self, api_client, one_product):
        resp = await api_client.delete(f"{self.API_URL}/{one_product.uid}")
        assert resp.status_code == 204
        new_resp = await api_client.get(f"{self.API_URL}/{one_product.uid}")
        assert new_resp.status_code == 404

    async def test_product_full_update(self, snapshot, api_client, one_product):
        resp = await api_client.put(
            self.API_URL + f"/{one_product.uid}",
            json={"name": "test-updated", "url": "test-url-updated", "price": "12"},
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    async def test_product_partial_update(self, snapshot, api_client, one_product):
        resp = await api_client.put(
            self.API_URL + f"/{one_product.uid}",
            json={"name": "test-partial-updated", "price": "11"},
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)
