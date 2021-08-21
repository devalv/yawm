# -*- coding: utf-8 -*-
"""Wishlist api tests."""

import pytest

from core.database import ProductGinoModel, WishlistGinoModel

pytestmark = [pytest.mark.asyncio, pytest.mark.api_full]

API_URL_PREFIX = "/v1"


@pytest.fixture
async def products_1(single_user):
    return await ProductGinoModel.create(
        user_id=single_user.id, name="test", url="https://devyatkin.dev/1"
    )


@pytest.fixture
async def products_9(single_user):
    products_list = list()
    for i in range(1, 10):
        product = await ProductGinoModel.create(
            user_id=single_user.id, name=f"test{i}", url=f"https://devyatkin.dev/{i}"
        )
        products_list.append(product)
    return products_list


@pytest.fixture
async def products_149(single_user):
    products_list = list()
    for i in range(1, 150):
        product = await ProductGinoModel.create(
            user_id=single_user.id, name=f"test{i}", url=f"https://devyatkin.dev/{i}"
        )
        products_list.append(product)
    return products_list


@pytest.fixture
async def ew_1(single_user):
    """1 empty wishlist."""
    wishlist = await WishlistGinoModel.create(user_id=single_user.id, name="test")
    return wishlist


@pytest.fixture
async def empty_wishlists_4(single_user):
    for i in range(1, 5):
        await WishlistGinoModel.create(user_id=single_user.id, name=f"test{i}")


@pytest.fixture
async def empty_wishlists_149(single_user):
    for i in range(1, 150):
        await WishlistGinoModel.create(user_id=single_user.id, name=f"test{i}")


@pytest.fixture
async def wishlist_products_1(ew_1, products_1):
    wishlist = await WishlistGinoModel.get(ew_1.id)
    return await wishlist.add_product(
        products_1.id, reserved=False, substitutable=False
    )


@pytest.fixture
async def wishlist_products_9(ew_1, products_9):
    products_list = list()
    wishlist = await WishlistGinoModel.get(ew_1.id)
    for product in products_9:
        rv = await wishlist.add_product(product.id, reserved=False, substitutable=True)
        products_list.append(rv)
    return products_list


@pytest.fixture
async def wp_149(ew_1, products_149):
    """149 wishlist products."""
    products_list = list()
    wishlist = await WishlistGinoModel.get(ew_1.id)
    for product in products_149:
        rv = await wishlist.add_product(product.id, reserved=False, substitutable=True)
        products_list.append(rv)
    return products_list


@pytest.mark.skip(reason="not implemented yet.")
async def test_trailing_slash(backend_app):
    """Test that trailing slash redirects working."""
    resp = await backend_app.get(f"{API_URL_PREFIX}/product/")
    assert resp.is_redirect
    assert resp.status_code == 307


class TestProduct:
    """Product API tests."""

    API_URL = f"{API_URL_PREFIX}/product"

    @pytest.mark.api_base
    async def test_product_create_no_auth(self, backend_app):
        resp = await backend_app.post(
            self.API_URL,
            json={
                "data": {
                    "attributes": {"name": "Product1", "url": "https://devyatkin.dev"}
                }
            },
        )
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_product_create(
        self, snapshot, backend_app, single_user_auth_headers
    ):
        resp = await backend_app.post(
            self.API_URL,
            json={
                "data": {
                    "attributes": {"name": "Product1", "url": "https://devyatkin.dev"}
                }
            },
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data.pop("id", None)
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_products(self, snapshot, backend_app, products_9):
        resp = await backend_app.get(self.API_URL)
        assert resp.status_code == 200
        resp_data = resp.json()

        assert isinstance(resp_data, dict)
        # removing product id from items
        resp_products = resp_data["data"]
        for resp_product in resp_products:
            assert "id" in resp_product
            assert "type" in resp_product
            resp_product.pop("id", None)
            assert "created_at" in resp_product["attributes"]
            assert "updated_at" in resp_product["attributes"]
            resp_product["attributes"].pop("created_at", None)
            resp_product["attributes"].pop("updated_at", None)

        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_product_read(self, snapshot, backend_app, products_1):
        resp = await backend_app.get(f"{self.API_URL}/{products_1.id}")
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_product_delete_no_auth(self, backend_app, products_1):
        resp = await backend_app.delete(f"{self.API_URL}/{products_1.id}")
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_product_delete_no_owner(
        self, backend_app, products_1, another_single_user_auth_headers
    ):
        resp = await backend_app.delete(
            f"{self.API_URL}/{products_1.id}", headers=another_single_user_auth_headers
        )
        assert resp.status_code == 403

    @pytest.mark.api_base
    async def test_product_delete_admin(
        self, backend_app, products_1, single_admin_auth_headers
    ):
        resp = await backend_app.delete(
            f"{self.API_URL}/{products_1.id}", headers=single_admin_auth_headers
        )
        assert resp.status_code == 204
        new_resp = await backend_app.get(
            f"{self.API_URL}/{products_1.id}", headers=single_admin_auth_headers
        )
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_product_delete(
        self, backend_app, products_1, single_user_auth_headers
    ):
        resp = await backend_app.delete(
            f"{self.API_URL}/{products_1.id}", headers=single_user_auth_headers
        )
        assert resp.status_code == 204
        new_resp = await backend_app.get(
            f"{self.API_URL}/{products_1.id}", headers=single_user_auth_headers
        )
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_product_full_update_no_auth(self, snapshot, backend_app, products_1):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={
                "data": {"attributes": {"name": "test-updated", "url": "https://ya.ru"}}
            },
        )
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_product_full_update_no_owner(
        self, snapshot, backend_app, products_1, another_single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={
                "data": {"attributes": {"name": "test-updated", "url": "https://ya.ru"}}
            },
            headers=another_single_user_auth_headers,
        )
        assert resp.status_code == 403

    @pytest.mark.api_base
    async def test_product_full_update_admin(
        self, snapshot, backend_app, products_1, single_admin_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={
                "data": {"attributes": {"name": "test-updated", "url": "https://ya.ru"}}
            },
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_product_full_update(
        self, snapshot, backend_app, products_1, single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={
                "data": {"attributes": {"name": "test-updated", "url": "https://ya.ru"}}
            },
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_json_data)

    async def test_product_partial_update_no_auth(
        self, snapshot, backend_app, products_1
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={"data": {"attributes": {"name": "partial-updated-name"}}},
        )
        assert resp.status_code == 401

    async def test_product_partial_update_no_owner(
        self, snapshot, backend_app, products_1, another_single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={"data": {"attributes": {"name": "partial-updated-name"}}},
            headers=another_single_user_auth_headers,
        )
        assert resp.status_code == 403

    async def test_product_partial_update_admin(
        self, snapshot, backend_app, products_1, single_admin_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={"data": {"attributes": {"name": "partial-updated-name"}}},
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_json_data)

    async def test_product_partial_update(
        self, snapshot, backend_app, products_1, single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={"data": {"attributes": {"name": "partial-updated-name"}}},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_product_paginator_limit(self, snapshot, backend_app, products_9):
        paginator_limit = 5
        resp = await backend_app.get(
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
            assert "created_at" in resp_product["attributes"]
            assert "updated_at" in resp_product["attributes"]
            resp_product["attributes"].pop("created_at", None)
            resp_product["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_json_data)


class TestEmptyWishlist:
    """Empty wishlist API tests."""

    API_URL = f"{API_URL_PREFIX}/wishlist"

    @pytest.mark.api_base
    async def test_wishlist_create_no_auth(self, snapshot, backend_app):
        resp = await backend_app.post(
            self.API_URL, json={"data": {"attributes": {"name": "Wishlist1"}}}
        )
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_wishlist_create(
        self, snapshot, backend_app, single_user_auth_headers
    ):
        resp = await backend_app.post(
            self.API_URL,
            json={"data": {"attributes": {"name": "Wishlist1"}}},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_delete_no_auth(self, backend_app, ew_1):
        resp = await backend_app.delete(f"{self.API_URL}/{ew_1.id}")
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_empty_wishlist_delete_no_owner(
        self, backend_app, ew_1, another_single_user_auth_headers
    ):
        resp = await backend_app.delete(
            f"{self.API_URL}/{ew_1.id}", headers=another_single_user_auth_headers
        )
        assert resp.status_code == 403

    @pytest.mark.api_base
    async def test_empty_wishlist_delete_admin(
        self, backend_app, ew_1, single_admin_auth_headers
    ):
        resp = await backend_app.delete(
            f"{self.API_URL}/{ew_1.id}", headers=single_admin_auth_headers
        )
        assert resp.status_code == 204
        new_resp = await backend_app.get(
            f"{self.API_URL}/{ew_1.id}", headers=single_admin_auth_headers
        )
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_empty_wishlist_delete(
        self, backend_app, ew_1, single_user_auth_headers
    ):
        resp = await backend_app.delete(
            f"{self.API_URL}/{ew_1.id}", headers=single_user_auth_headers
        )
        assert resp.status_code == 204
        new_resp = await backend_app.get(
            f"{self.API_URL}/{ew_1.id}", headers=single_user_auth_headers
        )
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_empty_wishlists(self, snapshot, backend_app, empty_wishlists_4):
        resp = await backend_app.get(self.API_URL)
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
            assert "created_at" in resp_product["attributes"]
            assert "updated_at" in resp_product["attributes"]
            resp_product["attributes"].pop("created_at", None)
            resp_product["attributes"].pop("updated_at", None)
        snapshot.assert_match(items)

    @pytest.mark.api_base
    async def test_empty_wishlists_paginator_limit(
        self, snapshot, backend_app, empty_wishlists_4
    ):
        paginator_limit = 2
        resp = await backend_app.get(
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
            assert "created_at" in resp_product["attributes"]
            assert "updated_at" in resp_product["attributes"]
            resp_product["attributes"].pop("created_at", None)
            resp_product["attributes"].pop("updated_at", None)
        snapshot.assert_match(items)

    @pytest.mark.api_base
    async def test_empty_wishlist_read(self, snapshot, backend_app, ew_1):
        resp = await backend_app.get(self.API_URL + f"/{ew_1.id}")
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_full_update(
        self, snapshot, backend_app, ew_1, single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{ew_1.id}",
            json={"data": {"attributes": {"name": "test-updated"}}},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_full_update_no_auth(self, backend_app, ew_1):
        resp = await backend_app.put(
            f"{self.API_URL}/{ew_1.id}",
            json={"data": {"attributes": {"name": "test-updated"}}},
        )
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_empty_wishlist_full_update_no_owner(
        self, backend_app, ew_1, another_single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{ew_1.id}", headers=another_single_user_auth_headers
        )
        assert resp.status_code == 403

    @pytest.mark.api_base
    async def test_empty_wishlist_full_update_admin(
        self, snapshot, backend_app, ew_1, single_admin_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{ew_1.id}",
            json={"data": {"attributes": {"name": "test-updated"}}},
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        assert "created_at" in resp_data["attributes"]
        assert "updated_at" in resp_data["attributes"]
        resp_data["attributes"].pop("created_at", None)
        resp_data["attributes"].pop("updated_at", None)
        snapshot.assert_match(resp_data)


class TestWishlist:
    """Wishlist API tests."""

    @pytest.mark.api_base
    async def test_add_product_wishlist_no_auth(self, backend_app, ew_1, products_9):
        for i, product in enumerate(products_9):
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
            expected_data["data"]["attributes"]["wishlist_id"] = f"{ew_1.id}"
            expected_data["data"]["type"] = "wishlist_products"
            resp = await backend_app.post(
                f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products", json=insert_data
            )

            assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_add_product_wishlist(
        self, backend_app, ew_1, products_9, single_user_auth_headers
    ):
        for i, product in enumerate(products_9):
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
            expected_data["data"]["attributes"]["wishlist_id"] = f"{ew_1.id}"
            expected_data["data"]["type"] = "wishlist_products"
            resp = await backend_app.post(
                f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products",
                json=insert_data,
                headers=single_user_auth_headers,
            )

            assert resp.status_code == 200
            resp_json_data = resp.json()
            resp_data = resp_json_data["data"]
            assert "id" in resp_data
            assert "type" in resp_data
            resp_data.pop("id", None)
            assert resp_json_data == expected_data

        # check all products in wishlist
        products_resp = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"
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
    async def test_delete_product_wishlist_no_auth(
        self, snapshot, backend_app, wishlist_products_1
    ):
        # check products count
        products_resp = await backend_app.get(f"{API_URL_PREFIX}/product")
        assert products_resp.status_code == 200
        assert products_resp.json()["total"] == 1
        # delete 1 wishlist products
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}"  # noqa: E501
        )
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_delete_product_wishlist_no_owner(
        self,
        snapshot,
        backend_app,
        wishlist_products_1,
        another_single_user_auth_headers,
    ):
        # check products count
        products_resp = await backend_app.get(f"{API_URL_PREFIX}/product")
        assert products_resp.status_code == 200
        assert products_resp.json()["total"] == 1
        # delete 1 wishlist products
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            headers=another_single_user_auth_headers,
        )
        assert resp.status_code == 403

    @pytest.mark.api_base
    async def test_delete_product_wishlist_admin(
        self, snapshot, backend_app, wishlist_products_1, single_admin_auth_headers
    ):
        # check products count
        products_resp = await backend_app.get(f"{API_URL_PREFIX}/product")
        assert products_resp.status_code == 200
        assert products_resp.json()["total"] == 1
        # delete 1 wishlist products
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 204
        # check all products in wishlist
        products_resp = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
        )
        assert products_resp.status_code == 200
        product_resp_data = products_resp.json()
        assert isinstance(product_resp_data, dict)
        total = product_resp_data["total"]
        assert total == 0
        # check products count
        products_resp = await backend_app.get(f"{API_URL_PREFIX}/product")
        assert products_resp.status_code == 200
        assert products_resp.json()["total"] == 1

    @pytest.mark.api_base
    async def test_delete_product_wishlist(
        self, snapshot, backend_app, wishlist_products_1, single_user_auth_headers
    ):
        # check products count
        products_resp = await backend_app.get(f"{API_URL_PREFIX}/product")
        assert products_resp.status_code == 200
        assert products_resp.json()["total"] == 1
        # delete 1 wishlist products
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 204
        # check all products in wishlist
        products_resp = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
        )
        assert products_resp.status_code == 200
        product_resp_data = products_resp.json()
        assert isinstance(product_resp_data, dict)
        total = product_resp_data["total"]
        assert total == 0
        # check products count
        products_resp = await backend_app.get(f"{API_URL_PREFIX}/product")
        assert products_resp.status_code == 200
        assert products_resp.json()["total"] == 1

    @pytest.mark.api_full
    async def test_delete_wishlist_with_products_no_auth(
        self, backend_app, wishlist_products_1
    ):
        # check that wpr have 1 record
        wpr = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
        )
        assert wpr.json()["total"] == 1
        # delete wishlist assigned to wpr
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}"
        )
        assert resp.status_code == 401

    @pytest.mark.api_full
    async def test_delete_wishlist_with_products_no_owner(
        self, backend_app, wishlist_products_1, another_single_user_auth_headers
    ):
        # check that wpr have 1 record
        wpr = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
        )
        assert wpr.json()["total"] == 1
        # delete wishlist assigned to wpr
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}",
            headers=another_single_user_auth_headers,
        )
        assert resp.status_code == 403

    @pytest.mark.api_full
    async def test_delete_wishlist_with_products_admin(
        self, backend_app, wishlist_products_1, single_admin_auth_headers
    ):
        # check that wpr have 1 record
        wpr = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
        )
        assert wpr.json()["total"] == 1
        # delete wishlist assigned to wpr
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}",
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 204
        # check that wishlist deleted
        new_resp = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}"
        )
        assert new_resp.status_code == 404
        # check that wpr deleted too
        wpr_2 = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
        )
        assert wpr_2.status_code == 404

    @pytest.mark.api_full
    async def test_delete_wishlist_with_products(
        self, backend_app, wishlist_products_1, single_user_auth_headers
    ):
        # check that wpr have 1 record
        wpr = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
        )
        assert wpr.json()["total"] == 1
        # delete wishlist assigned to wpr
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}",
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 204
        # check that wishlist deleted
        new_resp = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}"
        )
        assert new_resp.status_code == 404
        # check that wpr deleted too
        wpr_2 = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
        )
        assert wpr_2.status_code == 404

    @pytest.mark.api_full
    async def test_delete_product_in_wishlist_no_auth(
        self, backend_app, wishlist_products_9
    ):
        # check that we have 9 products
        initial_products = await backend_app.get(f"{API_URL_PREFIX}/product")
        initial_products_total = initial_products.json()["total"]
        initial_products_total == 9
        #
        first_product = wishlist_products_9[0]
        # check that wpr exists
        wpr = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{first_product.wishlist_id}/products"
        )
        assert wpr.json()["total"] == 9
        # delete one of product

        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/product/{first_product.product_id}"
        )
        assert resp.status_code == 401

    @pytest.mark.api_full
    async def test_delete_product_in_wishlist_no_owner(
        self, backend_app, wishlist_products_9, another_single_user_auth_headers
    ):
        # check that we have 9 products
        initial_products = await backend_app.get(f"{API_URL_PREFIX}/product")
        initial_products_total = initial_products.json()["total"]
        initial_products_total == 9
        #
        first_product = wishlist_products_9[0]
        # check that wpr exists
        wpr = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{first_product.wishlist_id}/products"
        )
        assert wpr.json()["total"] == 9
        # delete one of product

        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/product/{first_product.product_id}",
            headers=another_single_user_auth_headers,
        )
        assert resp.status_code == 403

    @pytest.mark.api_full
    async def test_delete_product_in_wishlist_admin(
        self, backend_app, wishlist_products_9, single_admin_auth_headers
    ):
        # check that we have 9 products
        initial_products = await backend_app.get(f"{API_URL_PREFIX}/product")
        initial_products_total = initial_products.json()["total"]
        initial_products_total == 9
        #
        first_product = wishlist_products_9[0]
        # check that wpr exists
        wpr = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{first_product.wishlist_id}/products"
        )
        assert wpr.json()["total"] == 9
        # delete one of product

        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/product/{first_product.product_id}",
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 204
        # check that record deleted
        new_resp = await backend_app.get(
            f"{API_URL_PREFIX}/product/{first_product.product_id}"
        )
        assert new_resp.status_code == 404
        # check that now we have 8 products
        reduced_products = await backend_app.get(f"{API_URL_PREFIX}/product")
        reduced_products_total = reduced_products.json()["total"]
        reduced_products_total == 8
        # check that wpr exists
        wpr_2 = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{first_product.wishlist_id}/products"
        )
        assert wpr_2.json()["total"] == 8

    @pytest.mark.api_full
    async def test_delete_product_in_wishlist(
        self, backend_app, wishlist_products_9, single_user_auth_headers
    ):
        # check that we have 9 products
        initial_products = await backend_app.get(f"{API_URL_PREFIX}/product")
        initial_products_total = initial_products.json()["total"]
        initial_products_total == 9
        #
        first_product = wishlist_products_9[0]
        # check that wpr exists
        wpr = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{first_product.wishlist_id}/products"
        )
        assert wpr.json()["total"] == 9
        # delete one of product

        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/product/{first_product.product_id}",
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 204
        # check that record deleted
        new_resp = await backend_app.get(
            f"{API_URL_PREFIX}/product/{first_product.product_id}"
        )
        assert new_resp.status_code == 404
        # check that now we have 8 products
        reduced_products = await backend_app.get(f"{API_URL_PREFIX}/product")
        reduced_products_total = reduced_products.json()["total"]
        reduced_products_total == 8
        # check that wpr exists
        wpr_2 = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{first_product.wishlist_id}/products"
        )
        assert wpr_2.json()["total"] == 8

    @pytest.mark.api_base
    async def test_wishlist_products_list(self, backend_app, wishlist_products_1):
        products_resp = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
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
        self, backend_app, ew_1, wishlist_products_9
    ):
        paginator_limit = 5
        products_resp = await backend_app.get(
            f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products",
            query_string=dict(size=paginator_limit),
        )
        assert products_resp.status_code == 200
        product_resp_json_data = products_resp.json()
        size = product_resp_json_data["size"]
        assert size == paginator_limit
        for product in product_resp_json_data["data"]:
            assert "id" in product
            assert "type" in product

    async def test_delete_fake_product_wishlist_no_auth(
        self, snapshot, backend_app, wishlist_products_1
    ):
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.product_id}"  # noqa: E501
        )
        assert resp.status_code == 401

    async def test_delete_fake_product_wishlist(
        self, snapshot, backend_app, wishlist_products_1, single_user_auth_headers
    ):
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.product_id}",  # noqa: E501
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 404

    async def test_add_fake_product_wishlist_no_auth(
        self, backend_app, ew_1, products_9
    ):
        insert_data = {
            "data": {
                "attributes": {
                    "product_id": f"{ew_1.id}",
                    "reserved": False,
                    "substitutable": True,
                }
            }
        }
        resp = await backend_app.post(
            f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products",  # noqa: E501
            json=insert_data,
        )

        assert resp.status_code == 401

    async def test_add_fake_product_wishlist(
        self, backend_app, ew_1, products_9, single_user_auth_headers
    ):
        insert_data = {
            "data": {
                "attributes": {
                    "product_id": f"{ew_1.id}",
                    "reserved": False,
                    "substitutable": True,
                }
            }
        }
        resp = await backend_app.post(
            f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products",  # noqa: E501
            json=insert_data,
            headers=single_user_auth_headers,
        )

        assert resp.status_code == 404

    @pytest.mark.api_base
    async def test_update_wishlist_product_no_auth(
        self, backend_app, wishlist_products_1
    ):
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"reserved": True}}},
        )
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_update_wishlist_product_no_owner(
        self, backend_app, wishlist_products_1, another_single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"reserved": True}}},
            headers=another_single_user_auth_headers,
        )
        assert resp.status_code == 403

    @pytest.mark.api_base
    async def test_update_wishlist_product_admin(
        self, backend_app, wishlist_products_1, single_admin_auth_headers
    ):
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"reserved": True}}},
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["reserved"] is True

    @pytest.mark.api_base
    async def test_update_wishlist_product(
        self, backend_app, wishlist_products_1, single_user_auth_headers
    ):
        assert not wishlist_products_1.substitutable
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True, "reserved": True}}},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["substitutable"] is True
        assert resp_data["attributes"]["reserved"] is True

    @pytest.mark.api_base
    async def test_reserve_wishlist_product(self, backend_app, wishlist_products_1):
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}/reserve",  # noqa: E501
            json={"data": {"attributes": {"reserved": True}}},
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["reserved"] is True

    async def test_reserve_fake_wishlist_product(
        self, backend_app, wishlist_products_1
    ):
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"reserved": True}}},
        )
        assert resp.status_code == 404

    @pytest.mark.api_base
    async def test_substitute_wishlist_product_no_auth(
        self, backend_app, wishlist_products_1
    ):
        assert not wishlist_products_1.substitutable
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
        )
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_substitute_wishlist_product_no_owner(
        self, backend_app, wishlist_products_1, another_single_user_auth_headers
    ):
        assert not wishlist_products_1.substitutable
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
            headers=another_single_user_auth_headers,
        )
        assert resp.status_code == 403

    @pytest.mark.api_base
    async def test_substitute_wishlist_product_admin(
        self, backend_app, wishlist_products_1, single_admin_auth_headers
    ):
        assert not wishlist_products_1.substitutable
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["substitutable"]

    @pytest.mark.api_base
    async def test_substitute_wishlist_product(
        self, backend_app, wishlist_products_1, single_user_auth_headers
    ):
        assert not wishlist_products_1.substitutable
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["substitutable"]

    async def test_substitute_fake_wishlist_product_no_auth(
        self, backend_app, wishlist_products_1
    ):
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
        )
        assert resp.status_code == 401

    async def test_substitute_fake_wishlist_product(
        self, backend_app, wishlist_products_1, single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 404


class PaginatorValidator:
    """Utils for validation dynamic paginator data"""

    @staticmethod
    def validate_links(
        links: dict,
        url: str,
        last_page_num: int,
        next_page_num: int,
        prev_page_num: int,
        self_page_num: int,
        size: int = None,
    ) -> None:
        # paginator url prefix
        if size is not None:
            pagination_url_prefix = f"{url}?size={size}&page="
        else:
            pagination_url_prefix = f"{url}?page="

        # validate pagination links values
        assert links["first"] == f"{pagination_url_prefix}1"

        if self_page_num is not None:
            try:
                assert links["self"] == f"{pagination_url_prefix}{self_page_num}"
            except AssertionError:
                assert f"page={self_page_num}" in links["self"]
                assert f"size={size}" in links["self"]
        elif size is not None:
            try:
                assert links["self"] == f"{url}?size={size}"
            except AssertionError:
                assert f"page={self_page_num}" in links["self"]
                assert f"size={size}" in links["self"]
        else:
            assert links["self"] == url

        if last_page_num is not None:
            try:
                assert links["last"] == f"{pagination_url_prefix}{last_page_num}"
            except AssertionError:
                assert f"page={self_page_num}" in links["last"]
                assert f"size={size}" in links["last"]
        else:
            assert links["last"] is None

        if next_page_num is not None:
            try:
                assert links["next"] == f"{pagination_url_prefix}{next_page_num}"
            except AssertionError:
                assert f"page={self_page_num}" in links["next"]
                assert f"size={size}" in links["next"]
        else:
            assert links["next"] is None

        if prev_page_num is not None:
            try:
                assert links["prev"] == f"{pagination_url_prefix}{prev_page_num}"
            except AssertionError:
                assert f"page={self_page_num}" in links["prev"]
                assert f"size={size}" in links["prev"]
        else:
            assert links["prev"] is None


class TestWPPaginator(PaginatorValidator):
    """Wishlist Products paginator extra tests."""

    @staticmethod
    def validate_response(json_data: dict) -> None:
        response_data = json_data["data"]
        for product in response_data:
            attributes = product["attributes"]
            assert "id" in product
            assert "wishlist_id" in attributes
            assert "product_id" in attributes
            product.pop("id", None)
            attributes.pop("wishlist_id", None)
            attributes.pop("product_id", None)

    @pytest.mark.api_full
    async def test_default_paginator(self, snapshot, backend_app, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open default page
        response = await backend_app.get(api_url)
        assert response.status_code == 200
        response_json_data = response.json()
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=2,
            prev_page_num=None,
            self_page_num=None,
        )
        # assert response data
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_next_page_paginator(self, snapshot, backend_app, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open next paginator page
        response = await backend_app.get(api_url, query_string=dict(page=2))
        assert response.status_code == 200
        response_json_data = response.json()
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=3,
            prev_page_num=1,
            self_page_num=2,
        )
        # check response data
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_first_page_paginator(self, snapshot, backend_app, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open first paginator page
        response = await backend_app.get(api_url, query_string=dict(page=1))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=2,
            prev_page_num=None,
            self_page_num=1,
        )
        # assert response data
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_paginator(self, snapshot, backend_app, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open last paginator page
        response = await backend_app.get(api_url, query_string=dict(page=3))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=None,
            prev_page_num=2,
            self_page_num=3,
        )
        # assert response data
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_reduced_qs_paginator(self, snapshot, backend_app, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # reduce QS size
        response = await backend_app.get(api_url, query_string=dict(size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=f"{api_url}",
            last_page_num=15,
            next_page_num=2,
            prev_page_num=None,
            self_page_num=None,
            size=10,
        )
        # assert response data
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_reduced_qs_paginator(
        self, snapshot, backend_app, ew_1, wp_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open last page with reduced QS size
        response = await backend_app.get(api_url, query_string=dict(page=15, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            size=10,
            last_page_num=15,
            next_page_num=None,
            prev_page_num=14,
            self_page_num=15,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_empty_page_reduced_qs_paginator(
        self, snapshot, backend_app, ew_1, wp_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open empty page with reduced QS size
        response = await backend_app.get(api_url, query_string=dict(page=16, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            size=10,
            last_page_num=15,
            next_page_num=None,
            prev_page_num=15,
            self_page_num=16,
        )
        snapshot.assert_match(response_json_data)


class TestProductPaginator(PaginatorValidator):
    """Products paginator extra tests."""

    @staticmethod
    def validate_response(json_data: dict):
        response_data = json_data["data"]
        for product in response_data:
            assert "id" in product
            product.pop("id", None)
        return json_data

    @pytest.mark.api_full
    async def test_default_paginator(self, snapshot, backend_app, products_149):
        api_url = f"{API_URL_PREFIX}/product"

        # open default page
        response = await backend_app.get(api_url)
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=2,
            prev_page_num=None,
            self_page_num=None,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_next_page_paginator(self, snapshot, backend_app, products_149):
        api_url = f"{API_URL_PREFIX}/product"
        # open next paginator page
        response = await backend_app.get(api_url, query_string=dict(page=2))
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=3,
            prev_page_num=1,
            self_page_num=2,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_first_page_paginator(self, snapshot, backend_app, products_149):
        api_url = f"{API_URL_PREFIX}/product"
        # open first paginator page
        response = await backend_app.get(api_url, query_string=dict(page=1))
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=2,
            prev_page_num=None,
            self_page_num=1,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_paginator(self, snapshot, backend_app, products_149):
        api_url = f"{API_URL_PREFIX}/product"
        # open last paginator page
        response = await backend_app.get(api_url, query_string=dict(page=3))
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=None,
            prev_page_num=2,
            self_page_num=3,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_reduced_qs_paginator(self, snapshot, backend_app, products_149):
        api_url = f"{API_URL_PREFIX}/product"
        # reduce QS size
        response = await backend_app.get(api_url, query_string=dict(size=10))
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            size=10,
            last_page_num=15,
            next_page_num=2,
            prev_page_num=None,
            self_page_num=None,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_reduced_qs_paginator(
        self, snapshot, backend_app, products_149
    ):
        api_url = f"{API_URL_PREFIX}/product"
        # open last page with reduced QS size
        response = await backend_app.get(api_url, query_string=dict(page=15, size=10))
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            size=10,
            last_page_num=15,
            next_page_num=None,
            prev_page_num=14,
            self_page_num=15,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_empty_page_reduced_qs_paginator(
        self, snapshot, backend_app, products_149
    ):
        api_url = f"{API_URL_PREFIX}/product"

        # open empty page with reduced QS size
        response = await backend_app.get(api_url, query_string=dict(page=16, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            size=10,
            last_page_num=15,
            next_page_num=None,
            prev_page_num=15,
            self_page_num=16,
        )
        snapshot.assert_match(response_json_data)


class TestWishlistPaginator(PaginatorValidator):
    """Wishlist paginator extra tests."""

    @staticmethod
    def validate_response(json_data: dict):
        response_data = json_data["data"]
        for product in response_data:
            assert "id" in product
            product.pop("id", None)
        return json_data

    @pytest.mark.api_full
    async def test_default_paginator(self, snapshot, backend_app, empty_wishlists_149):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open default page
        response = await backend_app.get(api_url)
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)

        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=2,
            prev_page_num=None,
            self_page_num=None,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_next_page_paginator(
        self, snapshot, backend_app, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open next paginator page
        response = await backend_app.get(api_url, query_string=dict(page=2))
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=3,
            prev_page_num=1,
            self_page_num=2,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_first_page_paginator(
        self, snapshot, backend_app, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open first paginator page
        response = await backend_app.get(api_url, query_string=dict(page=1))
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=2,
            prev_page_num=None,
            self_page_num=1,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_paginator(
        self, snapshot, backend_app, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open last paginator page
        response = await backend_app.get(api_url, query_string=dict(page=3))
        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            last_page_num=3,
            next_page_num=None,
            prev_page_num=2,
            self_page_num=3,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_reduced_qs_paginator(
        self, snapshot, backend_app, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # reduce QS size
        response = await backend_app.get(api_url, query_string=dict(size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            size=10,
            last_page_num=15,
            next_page_num=2,
            prev_page_num=None,
            self_page_num=None,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_reduced_qs_paginator(
        self, snapshot, backend_app, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open last page with reduced QS size
        response = await backend_app.get(api_url, query_string=dict(page=15, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        for row in response_json_data["data"]:
            assert "created_at" in row["attributes"]
            assert "updated_at" in row["attributes"]
            row["attributes"].pop("created_at", None)
            row["attributes"].pop("updated_at", None)
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            size=10,
            last_page_num=15,
            next_page_num=None,
            prev_page_num=14,
            self_page_num=15,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_empty_page_reduced_qs_paginator(
        self, snapshot, backend_app, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open empty page with reduced QS size
        response = await backend_app.get(api_url, query_string=dict(page=16, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        # check pagination links
        self.validate_links(
            response_json_data.pop("links"),
            url=api_url,
            size=10,
            last_page_num=15,
            next_page_num=None,
            prev_page_num=15,
            self_page_num=16,
        )
        snapshot.assert_match(response_json_data)
