# -*- coding: utf-8 -*-
"""Wishlist api tests."""
from core.database import ProductGinoModel, WishlistGinoModel

import pytest

pytestmark = [pytest.mark.asyncio, pytest.mark.api_full]

API_URL_PREFIX = "/api/v1"


@pytest.fixture()
async def nine_products():
    products_list = list()
    for i in range(1, 10):
        product = await ProductGinoModel.create(
            name=f"test{i}", url=f"https://devyatkin.dev/{i}"
        )
        products_list.append(product)
    return products_list


@pytest.fixture()
async def one_product():
    product = await ProductGinoModel.create(name="test", url="https://devyatkin.dev/1")
    return product


@pytest.fixture()
async def one_empty_wishlist():
    wishlist = await WishlistGinoModel.create(name="test")
    return wishlist


@pytest.fixture()
async def one_product_wishlist(one_empty_wishlist, one_product):
    wishlist = await WishlistGinoModel.get(one_empty_wishlist.id)
    return await wishlist.add_product(
        one_product.id, reserved=False, substitutable=False
    )


@pytest.fixture()
async def nine_products_wishlist(one_empty_wishlist, nine_products):
    products_list = list()
    wishlist = await WishlistGinoModel.get(one_empty_wishlist.id)
    for product in nine_products:
        rv = await wishlist.add_product(product.id, reserved=False, substitutable=True)
        products_list.append(rv)
    return products_list


@pytest.fixture()
async def _four_empty_wishlists():
    for i in range(1, 5):
        await WishlistGinoModel.create(name=f"test{i}")


@pytest.mark.skip(reason="not implemented yet.")
async def test_trailing_slash(api_client):
    """Test that trailing slash redirects working."""
    resp = await api_client.get(f"{API_URL_PREFIX}/product/")
    assert resp.is_redirect
    assert resp.status_code == 307


class TestProduct:
    """Product API tests."""

    API_URL = f"{API_URL_PREFIX}/product"

    @pytest.mark.api_base
    async def test_product_create(self, snapshot, api_client):
        resp = await api_client.post(
            self.API_URL,
            json={
                "data": {
                    "attributes": {"name": "Product1", "url": "https://devyatkin.dev"}
                }
            },
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_products(self, snapshot, api_client, nine_products):
        resp = await api_client.get(self.API_URL)
        assert resp.status_code == 200
        resp_data = resp.json()
        assert isinstance(resp_data, dict)
        # removing product id from items
        resp_products = resp_data["data"]
        for resp_product in resp_products:
            assert "id" in resp_product
            assert "type" in resp_product
            resp_product.pop("id", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_product_read(self, snapshot, api_client, one_product):
        resp = await api_client.get(f"{self.API_URL}/{one_product.id}")
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_product_delete(self, api_client, one_product):
        resp = await api_client.delete(f"{self.API_URL}/{one_product.id}")
        assert resp.status_code == 204
        new_resp = await api_client.get(f"{self.API_URL}/{one_product.id}")
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_product_full_update(self, snapshot, api_client, one_product):
        resp = await api_client.put(
            f"{self.API_URL}/{one_product.id}",
            json={
                "data": {"attributes": {"name": "test-updated", "url": "https://ya.ru"}}
            },
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        snapshot.assert_match(resp_json_data)

    async def test_product_partial_update(self, snapshot, api_client, one_product):
        resp = await api_client.put(
            f"{self.API_URL}/{one_product.id}",
            json={"data": {"attributes": {"name": "partial-updated-name"}}},
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_product_paginator_limit(self, snapshot, api_client, nine_products):
        paginator_limit = 5
        resp = await api_client.get(
            self.API_URL, query_string=dict(size=paginator_limit)
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert len(resp_data) == paginator_limit
        for resp_product in resp_data:
            assert "id" in resp_product
            assert "type" in resp_product
            resp_product.pop("id", None)
        snapshot.assert_match(resp_json_data)


class TestEmptyWishlist:
    """Empty wishlist API tests."""

    API_URL = f"{API_URL_PREFIX}/wishlist"

    @pytest.mark.api_base
    async def test_wishlist_create(self, snapshot, api_client):
        resp = await api_client.post(
            self.API_URL, json={"data": {"attributes": {"name": "Wishlist1"}}}
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_delete(self, api_client, one_empty_wishlist):
        resp = await api_client.delete(f"{self.API_URL}/{one_empty_wishlist.id}")
        assert resp.status_code == 204
        new_resp = await api_client.get(f"{self.API_URL}/{one_empty_wishlist.id}")
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_empty_wishlists(self, snapshot, api_client, _four_empty_wishlists):
        resp = await api_client.get(self.API_URL)
        assert resp.status_code == 200
        resp_json_data = resp.json()
        assert isinstance(resp_json_data, dict)
        items = resp_json_data["data"]
        count = resp_json_data["total"]
        assert count == 4
        # remove unique data from fetch
        for resp_product in items:
            assert "id" in resp_product
            assert "type" in resp_product
            resp_product.pop("id", None)
        snapshot.assert_match(items)

    @pytest.mark.api_base
    async def test_empty_wishlists_paginator_limit(
        self, snapshot, api_client, _four_empty_wishlists
    ):
        paginator_limit = 2
        resp = await api_client.get(
            self.API_URL, query_string=dict(size=paginator_limit)
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert isinstance(resp_data, dict)
        items = resp_data["data"]
        size = resp_data["size"]
        total = resp_data["total"]
        assert size == paginator_limit
        assert total == 4
        # remove unique data from fetch
        for resp_product in items:
            assert "id" in resp_product
            assert "type" in resp_product
            resp_product.pop("id", None)
        snapshot.assert_match(items)

    @pytest.mark.api_base
    async def test_empty_wishlist_read(self, snapshot, api_client, one_empty_wishlist):
        resp = await api_client.get(self.API_URL + f"/{one_empty_wishlist.id}")
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_full_update(
        self, snapshot, api_client, one_empty_wishlist
    ):
        resp = await api_client.put(
            f"{self.API_URL}/{one_empty_wishlist.id}",
            json={"data": {"attributes": {"name": "test-updated"}}},
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
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
                "data": {
                    "attributes": {
                        "product_id": f"{product.id}",
                        "reserved": False,
                        "substitutable": True,
                    }
                }
            }
            expected_data = insert_data.copy()
            expected_data["data"]["attributes"][
                "wishlist_id"
            ] = f"{one_empty_wishlist.id}"
            expected_data["data"]["type"] = "wishlist_products"
            resp = await api_client.post(
                f"{API_URL_PREFIX}/wishlist/{one_empty_wishlist.id}/products",
                json=insert_data,
            )

            assert resp.status_code == 200
            resp_json_data = resp.json()
            resp_data = resp_json_data["data"]
            assert "id" in resp_data
            assert "type" in resp_data
            resp_data.pop("id", None)
            assert resp_json_data == expected_data

        # check all products in wishlist
        products_resp = await api_client.get(
            f"{API_URL_PREFIX}/wishlist/{one_empty_wishlist.id}/products"
        )

        assert products_resp.status_code == 200
        product_resp_json_data = products_resp.json()
        product_resp_data = product_resp_json_data["data"]
        for product in product_resp_data:
            assert "id" in product
            assert "type" in product
        total = product_resp_json_data["total"]
        assert total == 9

    @pytest.mark.api_base
    async def test_delete_product_wishlist(
        self, snapshot, api_client, one_product_wishlist
    ):
        resp = await api_client.delete(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.wishlist_id}/products/{one_product_wishlist.id}"  # noqa: E501
        )

        assert resp.status_code == 204

        # check all products in wishlist
        products_resp = await api_client.get(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.wishlist_id}/products"
        )
        assert products_resp.status_code == 200
        product_resp_data = products_resp.json()
        assert isinstance(product_resp_data, dict)
        total = product_resp_data["total"]
        assert total == 0

    @pytest.mark.skip(reason="not implemented yet.")
    async def test_delete_wishlist_with_products(
        self, api_client, one_product_wishlist
    ):
        # TODO: maybe make validation error?
        resp = await api_client.delete(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.wishlist_id}"
        )
        assert resp.status_code == 204
        new_resp = await api_client.get(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.wishlist_id}"
        )
        assert new_resp.status_code == 404

    @pytest.mark.skip(reason="not implemented yet.")
    async def test_delete_product_in_wishlist(self, api_client, one_product_wishlist):
        # TODO: maybe make validation error?
        resp = await api_client.delete(
            f"{API_URL_PREFIX}/products/{one_product_wishlist.product_id}"
        )
        assert resp.status_code == 204
        new_resp = await api_client.get(
            f"{API_URL_PREFIX}/products/{one_product_wishlist.product_id}"
        )
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_wishlist_products_list(self, api_client, one_product_wishlist):
        products_resp = await api_client.get(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.wishlist_id}/products"
        )
        assert products_resp.status_code == 200
        product_resp_json_data = products_resp.json()
        total = product_resp_json_data["total"]
        assert total == 1

        product_resp_data = product_resp_json_data["data"]
        for product in product_resp_data:
            assert "id" in product
            assert "type" in product

    @pytest.mark.api_base
    async def test_paginator_wishlist_products_list(
        self, api_client, one_empty_wishlist, nine_products_wishlist
    ):
        paginator_limit = 5
        products_resp = await api_client.get(
            f"{API_URL_PREFIX}/wishlist/{one_empty_wishlist.id}/products",
            query_string=dict(size=paginator_limit),
        )
        assert products_resp.status_code == 200
        product_resp_json_data = products_resp.json()
        size = product_resp_json_data["size"]
        assert size == paginator_limit
        for product in product_resp_json_data["data"]:
            assert "id" in product
            assert "type" in product

    async def test_delete_fake_product_wishlist(
        self, snapshot, api_client, one_product_wishlist
    ):
        resp = await api_client.delete(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.wishlist_id}/products/{one_product_wishlist.product_id}"  # noqa: E501
        )
        assert resp.status_code == 404

    async def test_add_fake_product_wishlist(
        self, api_client, one_empty_wishlist, nine_products
    ):
        insert_data = {
            "data": {
                "attributes": {
                    "product_id": f"{one_empty_wishlist.id}",
                    "reserved": False,
                    "substitutable": True,
                }
            }
        }
        resp = await api_client.post(
            f"{API_URL_PREFIX}/wishlist/{one_empty_wishlist.id}/products",  # noqa: E501
            json=insert_data,
        )

        assert resp.status_code == 404

    @pytest.mark.api_base
    async def test_reserve_wishlist_product(self, api_client, one_product_wishlist):
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.wishlist_id}/products/{one_product_wishlist.id}",  # noqa: E501
            json={"data": {"attributes": {"reserved": True}}},
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["reserved"] is True

    @pytest.mark.api_base
    async def test_substitute_wishlist_product(self, api_client, one_product_wishlist):
        assert not one_product_wishlist.substitutable
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.wishlist_id}/products/{one_product_wishlist.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["substitutable"]

    @pytest.mark.api_base
    async def test_update_wishlist_product(self, api_client, one_product_wishlist):
        assert not one_product_wishlist.substitutable
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.wishlist_id}/products/{one_product_wishlist.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True, "reserved": True}}},
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["substitutable"] is True
        assert resp_data["attributes"]["reserved"] is True

    async def test_reserve_fake_wishlist_product(
        self, api_client, one_product_wishlist
    ):
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.id}/products/{one_product_wishlist.id}",  # noqa: E501
            json={"data": {"attributes": {"reserved": True}}},
        )
        assert resp.status_code == 404

    async def test_substitute_fake_wishlist_product(
        self, api_client, one_product_wishlist
    ):
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{one_product_wishlist.id}/products/{one_product_wishlist.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
        )
        assert resp.status_code == 404


class TestPaginator:
    """Extended paginator tests."""

    pass
