# -*- coding: utf-8 -*-
"""Wishlist api tests."""
from core.database import ProductGinoModel, WishlistGinoModel

import pytest

pytestmark = [pytest.mark.asyncio, pytest.mark.api_full]

API_URL_PREFIX = "/api/v1"


@pytest.fixture()
async def products_1():
    return await ProductGinoModel.create(name="test", url="https://devyatkin.dev/1")


@pytest.fixture()
async def products_9():
    products_list = list()
    for i in range(1, 10):
        product = await ProductGinoModel.create(
            name=f"test{i}", url=f"https://devyatkin.dev/{i}"
        )
        products_list.append(product)
    return products_list


@pytest.fixture()
async def products_149():
    products_list = list()
    for i in range(1, 150):
        product = await ProductGinoModel.create(
            name=f"test{i}", url=f"https://devyatkin.dev/{i}"
        )
        products_list.append(product)
    return products_list


@pytest.fixture()
async def ew_1():
    """1 empty wishlist."""
    wishlist = await WishlistGinoModel.create(name="test")
    return wishlist


@pytest.fixture()
async def empty_wishlists_4():
    for i in range(1, 5):
        await WishlistGinoModel.create(name=f"test{i}")


@pytest.fixture()
async def empty_wishlists_149():
    for i in range(1, 150):
        await WishlistGinoModel.create(name=f"test{i}")


@pytest.fixture()
async def wishlist_products_1(ew_1, products_1):
    wishlist = await WishlistGinoModel.get(ew_1.id)
    return await wishlist.add_product(
        products_1.id, reserved=False, substitutable=False
    )


@pytest.fixture()
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
    async def test_products(self, snapshot, api_client, products_9):
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
    async def test_product_read(self, snapshot, api_client, products_1):
        resp = await api_client.get(f"{self.API_URL}/{products_1.id}")
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        snapshot.assert_match(resp_json_data)

    @pytest.mark.api_base
    async def test_product_delete(self, api_client, products_1):
        resp = await api_client.delete(f"{self.API_URL}/{products_1.id}")
        assert resp.status_code == 204
        new_resp = await api_client.get(f"{self.API_URL}/{products_1.id}")
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_product_full_update(self, snapshot, api_client, products_1):
        resp = await api_client.put(
            f"{self.API_URL}/{products_1.id}",
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

    async def test_product_partial_update(self, snapshot, api_client, products_1):
        resp = await api_client.put(
            f"{self.API_URL}/{products_1.id}",
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
    async def test_product_paginator_limit(self, snapshot, api_client, products_9):
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
    async def test_empty_wishlist_delete(self, api_client, ew_1):
        resp = await api_client.delete(f"{self.API_URL}/{ew_1.id}")
        assert resp.status_code == 204
        new_resp = await api_client.get(f"{self.API_URL}/{ew_1.id}")
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_empty_wishlists(self, snapshot, api_client, empty_wishlists_4):
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
        self, snapshot, api_client, empty_wishlists_4
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
    async def test_empty_wishlist_read(self, snapshot, api_client, ew_1):
        resp = await api_client.get(self.API_URL + f"/{ew_1.id}")
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        resp_data.pop("id", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_full_update(self, snapshot, api_client, ew_1):
        resp = await api_client.put(
            f"{self.API_URL}/{ew_1.id}",
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
    async def test_add_product_wishlist(self, api_client, ew_1, products_9):
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
            resp = await api_client.post(
                f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products", json=insert_data
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
    async def test_delete_product_wishlist(
        self, snapshot, api_client, wishlist_products_1
    ):
        # check products count
        products_resp = await api_client.get(f"{API_URL_PREFIX}/product")
        assert products_resp.status_code == 200
        assert products_resp.json()["total"] == 1
        # delete 1 wishlist products
        resp = await api_client.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}"  # noqa: E501
        )
        assert resp.status_code == 204
        # check all products in wishlist
        products_resp = await api_client.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products"
        )
        assert products_resp.status_code == 200
        product_resp_data = products_resp.json()
        assert isinstance(product_resp_data, dict)
        total = product_resp_data["total"]
        assert total == 0
        # check products count
        products_resp = await api_client.get(f"{API_URL_PREFIX}/product")
        assert products_resp.status_code == 200
        assert products_resp.json()["total"] == 1

    @pytest.mark.skip(reason="not implemented yet.")
    async def test_delete_wishlist_with_products(self, api_client, wishlist_products_1):
        # TODO: maybe make validation error?
        resp = await api_client.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}"
        )
        assert resp.status_code == 204
        new_resp = await api_client.get(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}"
        )
        assert new_resp.status_code == 404

    @pytest.mark.skip(reason="not implemented yet.")
    async def test_delete_product_in_wishlist(self, api_client, wishlist_products_1):
        # TODO: maybe make validation error?
        resp = await api_client.delete(
            f"{API_URL_PREFIX}/products/{wishlist_products_1.product_id}"
        )
        assert resp.status_code == 204
        new_resp = await api_client.get(
            f"{API_URL_PREFIX}/products/{wishlist_products_1.product_id}"
        )
        assert new_resp.status_code == 404

    @pytest.mark.api_base
    async def test_wishlist_products_list(self, api_client, wishlist_products_1):
        products_resp = await api_client.get(
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
        self, api_client, ew_1, wishlist_products_9
    ):
        paginator_limit = 5
        products_resp = await api_client.get(
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

    async def test_delete_fake_product_wishlist(
        self, snapshot, api_client, wishlist_products_1
    ):
        resp = await api_client.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.product_id}"  # noqa: E501
        )
        assert resp.status_code == 404

    async def test_add_fake_product_wishlist(self, api_client, ew_1, products_9):
        insert_data = {
            "data": {
                "attributes": {
                    "product_id": f"{ew_1.id}",
                    "reserved": False,
                    "substitutable": True,
                }
            }
        }
        resp = await api_client.post(
            f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products",  # noqa: E501
            json=insert_data,
        )

        assert resp.status_code == 404

    @pytest.mark.api_base
    async def test_reserve_wishlist_product(self, api_client, wishlist_products_1):
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"reserved": True}}},
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["reserved"] is True

    @pytest.mark.api_base
    async def test_substitute_wishlist_product(self, api_client, wishlist_products_1):
        assert not wishlist_products_1.substitutable
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["substitutable"]

    @pytest.mark.api_base
    async def test_update_wishlist_product(self, api_client, wishlist_products_1):
        assert not wishlist_products_1.substitutable
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True, "reserved": True}}},
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["data"]
        assert "id" in resp_data
        assert "type" in resp_data
        assert resp_data["attributes"]["substitutable"] is True
        assert resp_data["attributes"]["reserved"] is True

    async def test_reserve_fake_wishlist_product(self, api_client, wishlist_products_1):
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"reserved": True}}},
        )
        assert resp.status_code == 404

    async def test_substitute_fake_wishlist_product(
        self, api_client, wishlist_products_1
    ):
        resp = await api_client.put(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.id}/products/{wishlist_products_1.id}",  # noqa: E501
            json={"data": {"attributes": {"substitutable": True}}},
        )
        assert resp.status_code == 404


class TestWPPaginator:
    """Wishlist Products paginator extra tests."""

    @staticmethod
    def validate_response(json_data: dict):
        response_data = json_data["data"]
        for product in response_data:
            attributes = product["attributes"]
            assert "id" in product
            assert "wishlist_id" in attributes
            assert "product_id" in attributes
            product.pop("id", None)
            attributes.pop("wishlist_id", None)
            attributes.pop("product_id", None)
        return json_data

    @pytest.mark.api_full
    async def test_default_paginator(self, snapshot, api_client, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open default page
        response = await api_client.get(api_url)
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_next_page_paginator(self, snapshot, api_client, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open next paginator page
        response = await api_client.get(api_url, query_string=dict(page=1))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_first_page_paginator(self, snapshot, api_client, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open first paginator page
        response = await api_client.get(api_url, query_string=dict(page=0))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_paginator(self, snapshot, api_client, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open last paginator page
        response = await api_client.get(api_url, query_string=dict(page=2))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_reduced_qs_paginator(self, snapshot, api_client, ew_1, wp_149):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # reduce QS size
        response = await api_client.get(api_url, query_string=dict(size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_reduced_qs_paginator(
        self, snapshot, api_client, ew_1, wp_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open last page with reduced QS size
        response = await api_client.get(api_url, query_string=dict(page=14, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_empty_page_reduced_qs_paginator(
        self, snapshot, api_client, ew_1, wp_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist/{ew_1.id}/products"

        # open empty page with reduced QS size
        response = await api_client.get(api_url, query_string=dict(page=15, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)


class TestProductPaginator:
    """Products paginator extra tests."""

    @staticmethod
    def validate_response(json_data: dict):
        response_data = json_data["data"]
        for product in response_data:
            assert "id" in product
            product.pop("id", None)
        return json_data

    @pytest.mark.api_full
    async def test_default_paginator(self, snapshot, api_client, products_149):
        api_url = f"{API_URL_PREFIX}/product"

        # open default page
        response = await api_client.get(api_url)
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_next_page_paginator(self, snapshot, api_client, products_149):
        api_url = f"{API_URL_PREFIX}/product"

        # open next paginator page
        response = await api_client.get(api_url, query_string=dict(page=1))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_first_page_paginator(self, snapshot, api_client, products_149):
        api_url = f"{API_URL_PREFIX}/product"

        # open first paginator page
        response = await api_client.get(api_url, query_string=dict(page=0))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_paginator(self, snapshot, api_client, products_149):
        api_url = f"{API_URL_PREFIX}/product"

        # open last paginator page
        response = await api_client.get(api_url, query_string=dict(page=2))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_reduced_qs_paginator(self, snapshot, api_client, products_149):
        api_url = f"{API_URL_PREFIX}/product"

        # reduce QS size
        response = await api_client.get(api_url, query_string=dict(size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_reduced_qs_paginator(
        self, snapshot, api_client, products_149
    ):
        api_url = f"{API_URL_PREFIX}/product"

        # open last page with reduced QS size
        response = await api_client.get(api_url, query_string=dict(page=14, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_empty_page_reduced_qs_paginator(
        self, snapshot, api_client, products_149
    ):
        api_url = f"{API_URL_PREFIX}/product"

        # open empty page with reduced QS size
        response = await api_client.get(api_url, query_string=dict(page=15, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)


class TestWishlistPaginator:
    """Wishlist paginator extra tests."""

    @staticmethod
    def validate_response(json_data: dict):
        response_data = json_data["data"]
        for product in response_data:
            assert "id" in product
            product.pop("id", None)
        return json_data

    @pytest.mark.api_full
    async def test_default_paginator(self, snapshot, api_client, empty_wishlists_149):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open default page
        response = await api_client.get(api_url)
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_next_page_paginator(self, snapshot, api_client, empty_wishlists_149):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open next paginator page
        response = await api_client.get(api_url, query_string=dict(page=1))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_first_page_paginator(
        self, snapshot, api_client, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open first paginator page
        response = await api_client.get(api_url, query_string=dict(page=0))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_paginator(self, snapshot, api_client, empty_wishlists_149):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open last paginator page
        response = await api_client.get(api_url, query_string=dict(page=2))
        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_reduced_qs_paginator(
        self, snapshot, api_client, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # reduce QS size
        response = await api_client.get(api_url, query_string=dict(size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_reduced_qs_paginator(
        self, snapshot, api_client, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open last page with reduced QS size
        response = await api_client.get(api_url, query_string=dict(page=14, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_empty_page_reduced_qs_paginator(
        self, snapshot, api_client, empty_wishlists_149
    ):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open empty page with reduced QS size
        response = await api_client.get(api_url, query_string=dict(page=15, size=10))

        assert response.status_code == 200
        response_json_data = response.json()
        self.validate_response(response_json_data)
        snapshot.assert_match(response_json_data)
