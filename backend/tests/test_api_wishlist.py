# -*- coding: utf-8 -*-
"""Wishlist api tests."""
from core.database import ProductGinoModel, WishlistGinoModel

import pytest

pytestmark = [pytest.mark.asyncio, pytest.mark.api_full]


@pytest.fixture()
async def nine_products():
    products_list = list()
    for i in range(1, 10):
        product = await ProductGinoModel.create(
            name=f"test{i}", url=f"test-url{i}", price=f"12{i}.3{i}"
        )
        products_list.append(product)
    return products_list


@pytest.fixture()
async def one_product():
    product = await ProductGinoModel.create(name="test", url="test-url", price="12.3")
    return product


@pytest.fixture()
async def one_empty_wishlist():
    wishlist = await WishlistGinoModel.create(name="test", slug="test-slug")
    return wishlist


@pytest.fixture()
async def one_product_wishlist(one_empty_wishlist, one_product):
    await WishlistGinoModel.get(one_empty_wishlist.uid)
    rv = await WishlistGinoModel.add_product(one_product.uid)
    return rv


@pytest.fixture()
async def nine_products_wishlist(one_empty_wishlist, nine_products):
    products_list = list()
    await WishlistGinoModel.get(one_empty_wishlist.uid)
    for product in nine_products:
        rv = await WishlistGinoModel.add_product(product.uid)
        products_list.append(rv)
    return products_list


@pytest.fixture()
async def _four_empty_wishlists():
    for i in range(1, 5):
        await WishlistGinoModel.create(name=f"test{i}", slug=f"test-slug{i}")


@pytest.mark.skip(reason="not implemented yet.")
async def test_trailing_slash(api_client):
    """Test that trailing slash redirects working."""
    resp = await api_client.get("/api/v1/products/")
    assert resp.is_redirect
    assert resp.status_code == 307


class TestProduct:
    """Product API tests."""

    API_URL = "/api/v1/products"

    @pytest.mark.api_base
    async def test_product_create(self, snapshot, api_client):
        resp = await api_client.post(
            self.API_URL,
            json={"name": "Product1", "url": "product1", "price": "123.99"},
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_products(self, snapshot, api_client, nine_products):
        resp = await api_client.get(self.API_URL)
        assert resp.status_code == 200
        resp_data = resp.json()
        for resp_product in resp_data:
            resp_product.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_product_read(self, snapshot, api_client, one_product):
        resp = await api_client.get(f"{self.API_URL}/{one_product.uid}")
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_product_delete(self, api_client, one_product):
        resp = await api_client.delete(f"{self.API_URL}/{one_product.uid}")
        assert resp.status_code == 204
        new_resp = await api_client.get(f"{self.API_URL}/{one_product.uid}")
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_product_full_update(self, snapshot, api_client, one_product):
        resp = await api_client.put(
            f"{self.API_URL}/{one_product.uid}",
            json={"name": "test-updated", "url": "test-url-updated", "price": "12"},
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.skip(reason="not implemented yet.")
    async def test_product_partial_update(self, snapshot, api_client, one_product):
        resp = await api_client.put(
            f"{self.API_URL}/{one_product.uid}",
            json={"name": "test-partial-updated", "price": "11"},
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_product_paginator_limit(self, snapshot, api_client, nine_products):
        paginator_limit = 5
        resp = await api_client.get(
            self.API_URL, query_string=dict(limit=paginator_limit)
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert len(resp_data) == paginator_limit
        for resp_product in resp_data:
            resp_product.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_product_paginator_offset(self, snapshot, api_client, nine_products):
        paginator_offset = 5
        resp = await api_client.get(
            self.API_URL, query_string=dict(offset=paginator_offset)
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        for resp_product in resp_data:
            resp_product.pop("uid", None)
        snapshot.assert_match(resp_data)


class TestEmptyWishlist:
    """Empty wishlist API tests."""

    API_URL = "/api/v1/wishlists"

    @pytest.mark.api_base
    async def test_wishlist_create(self, snapshot, api_client):
        resp = await api_client.post(
            self.API_URL, json={"name": "Wishlist1", "slug": "wishlist1"}
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_delete(self, api_client, one_empty_wishlist):
        resp = await api_client.delete(f"{self.API_URL}/{one_empty_wishlist.uid}")
        assert resp.status_code == 204
        new_resp = await api_client.get(f"{self.API_URL}/{one_empty_wishlist.uid}")
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_empty_wishlists(self, snapshot, api_client, _four_empty_wishlists):
        resp = await api_client.get(self.API_URL)
        assert resp.status_code == 200
        resp_data = resp.json()
        for resp_product in resp_data:
            resp_product.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlists_paginator_limit(
        self, snapshot, api_client, _four_empty_wishlists
    ):
        paginator_limit = 2
        resp = await api_client.get(
            self.API_URL, query_string={"limit": paginator_limit}
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert len(resp_data) == paginator_limit
        for resp_product in resp_data:
            resp_product.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlists_paginator_offset(
        self, snapshot, api_client, _four_empty_wishlists
    ):
        paginator_offset = 2
        resp = await api_client.get(
            self.API_URL, query_string={"offset": paginator_offset}
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        for resp_product in resp_data:
            resp_product.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_read(self, snapshot, api_client, one_empty_wishlist):
        resp = await api_client.get(self.API_URL + f"/{one_empty_wishlist.uid}")
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.skip(reason="not implemented yet.")
    async def test_empty_wishlist_partial_update(
        self, snapshot, api_client, one_empty_wishlist
    ):
        resp = await api_client.put(
            f"{self.API_URL}/{one_empty_wishlist.uid}",
            json={"slug": "test-slug-updated"},
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_full_update(
        self, snapshot, api_client, one_empty_wishlist
    ):
        resp = await api_client.put(
            f"{self.API_URL}/{one_empty_wishlist.uid}",
            json={"name": "test-updated", "slug": "test-slug-updated"},
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        resp_data.pop("uid", None)
        snapshot.assert_match(resp_data)


class TestWishlist:
    """Wishlist API tests."""

    @pytest.mark.api_base
    async def test_add_product_wishlist(
        self, api_client, one_empty_wishlist, nine_products
    ):
        """

        :type nine_products: list
        """
        for i, product in enumerate(nine_products):
            insert_data = {
                "product_uid": f"{product.uid}",
                "wishlist_uid": f"{one_empty_wishlist.uid}",
            }
            resp = await api_client.post("/api/v1/products-wishlist", json=insert_data)

            assert resp.status_code == 200
            resp_data = resp.json()
            resp_data.pop("uid", None)
            resp_data.pop("reserved", None)
            assert resp_data == insert_data

            # check all products in wishlist
            products_resp = await api_client.get(
                f"/api/v1/wishlists/{one_empty_wishlist.uid}/products"
            )
            assert products_resp.status_code == 200
            assert len(products_resp.json()) == i + 1

    @pytest.mark.api_base
    async def test_delete_product_wishlist(
        self, snapshot, api_client, one_product_wishlist
    ):
        resp = await api_client.delete(
            f"/api/v1/products-wishlist/{one_product_wishlist.uid}"
        )
        assert resp.status_code == 204

        # check all products in wishlist
        products_resp = await api_client.get(
            f"/api/v1/wishlists/{one_product_wishlist.wishlist_uid}/products"
        )
        assert products_resp.status_code == 200
        assert products_resp.json() == list()

    @pytest.mark.skip(reason="not implemented yet.")
    async def test_delete_wishlist_with_products(
        self, api_client, one_product_wishlist
    ):
        # TODO: maybe make validation error?
        resp = await api_client.delete(
            f"/api/v1/wishlists/{one_product_wishlist.wishlist_uid}"
        )
        assert resp.status_code == 204
        new_resp = await api_client.get(
            f"/api/v1/wishlists/{one_product_wishlist.wishlist_uid}"
        )
        assert new_resp.status_code == 404

    @pytest.mark.skip(reason="not implemented yet.")
    async def test_delete_product_in_wishlist(self, api_client, one_product_wishlist):
        # TODO: maybe make validation error?
        resp = await api_client.delete(
            f"/api/v1/products/{one_product_wishlist.product_uid}"
        )
        assert resp.status_code == 204
        new_resp = await api_client.get(
            f"/api/v1/products/{one_product_wishlist.product_uid}"
        )
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_wishlist_products_list(self, api_client, one_product_wishlist):
        products_resp = await api_client.get(
            f"/api/v1/wishlists/{one_product_wishlist.wishlist_uid}/products"
        )
        assert products_resp.status_code == 200
        assert len(products_resp.json()) == 1

    @pytest.mark.api_base
    async def test_paginator_wishlist_products_list(
        self, api_client, one_empty_wishlist, nine_products_wishlist
    ):
        paginator_limit = 5
        products_resp = await api_client.get(
            f"/api/v1/wishlists/{one_empty_wishlist.uid}/products",
            query_string=dict(limit=paginator_limit),
        )
        assert products_resp.status_code == 200
        assert len(products_resp.json()) == paginator_limit

    @pytest.mark.api_base
    async def test_offset_wishlist_products_list(
        self, snapshot, api_client, one_empty_wishlist, nine_products_wishlist
    ):
        paginator_offset = 5
        products_resp = await api_client.get(
            f"/api/v1/wishlists/{one_empty_wishlist.uid}/products",
            query_string=dict(offset=paginator_offset),
        )
        assert products_resp.status_code == 200
        resp_data = products_resp.json()
        for resp_product in resp_data:
            resp_product.pop("uid", None)
        snapshot.assert_match(resp_data)

    async def test_delete_fake_product_wishlist(
        self, snapshot, api_client, one_product_wishlist
    ):
        resp = await api_client.delete(
            f"/api/v1/products-wishlist/{one_product_wishlist.product_uid}"
        )
        assert resp.status_code == 404

    async def test_add_fake_product_wishlist(
        self, api_client, one_empty_wishlist, nine_products
    ):
        insert_data = {
            "product_uid": f"{one_empty_wishlist.uid}",
            "wishlist_uid": f"{one_empty_wishlist.uid}",
        }
        resp = await api_client.post("/api/v1/products-wishlist", json=insert_data)
        assert resp.status_code == 404

    @pytest.mark.api_base
    async def test_reserve_wishlist_product(self, api_client, one_product_wishlist):
        resp = await api_client.put(
            f"/api/v1/products-wishlist/{one_product_wishlist.uid}",
            json={"reserved": True},
        )
        assert resp.status_code == 200
        assert resp.json()["reserved"] is True

    async def test_reserve_fake_wishlist_product(
        self, api_client, one_product_wishlist
    ):
        resp = await api_client.put(
            f"/api/v1/products-wishlist/{one_product_wishlist.product_uid}",
            json={"reserved": True},
        )
        assert resp.status_code == 404
