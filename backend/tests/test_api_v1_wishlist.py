# -*- coding: utf-8 -*-
"""Wishlist api tests."""

import pytest
import pytest_asyncio

from core.database import ProductGinoModel, WishlistGinoModel

pytestmark = [pytest.mark.asyncio, pytest.mark.api_full]

API_URL_PREFIX = "/api/v1"


@pytest_asyncio.fixture
async def products_1(single_user):
    return await ProductGinoModel.create(
        user_id=single_user.id, name="test", url="https://devyatkin.dev/1"
    )


@pytest_asyncio.fixture
async def products_9(single_user):
    products_list = list()
    for i in range(1, 10):
        product = await ProductGinoModel.create(
            user_id=single_user.id, name=f"test{i}", url=f"https://devyatkin.dev/{i}"
        )
        products_list.append(product)
    return products_list


@pytest_asyncio.fixture
async def products_149(single_user):
    products_list = list()
    for i in range(1, 150):
        product = await ProductGinoModel.create(
            user_id=single_user.id, name=f"test{i}", url=f"https://devyatkin.dev/{i}"
        )
        products_list.append(product)
    return products_list


@pytest_asyncio.fixture
async def ew_1(single_user):
    """1 empty wishlist."""
    wishlist = await WishlistGinoModel.create(user_id=single_user.id, name="test")
    return wishlist


@pytest_asyncio.fixture
async def empty_wishlists_4(single_user):
    for i in range(1, 5):
        await WishlistGinoModel.create(user_id=single_user.id, name=f"test{i}")


@pytest_asyncio.fixture
async def empty_wishlists_149(single_user):
    for i in range(1, 150):
        await WishlistGinoModel.create(user_id=single_user.id, name=f"test{i}")


@pytest_asyncio.fixture
async def wishlist_products_1(ew_1, products_1):
    wishlist = await WishlistGinoModel.get(ew_1.id)
    return await wishlist.add_product(
        products_1.id, reserved=False, substitutable=False, product_name=products_1.name
    )


@pytest_asyncio.fixture
async def wishlist_products_9(ew_1, products_9):
    products_list = list()
    wishlist = await WishlistGinoModel.get(ew_1.id)
    for product in products_9:
        rv = await wishlist.add_product(
            product.id, reserved=False, substitutable=True, product_name=product.name
        )
        products_list.append(rv)
    return products_list


@pytest_asyncio.fixture
async def wp_149(ew_1, products_149):
    """149 wishlist products."""
    products_list = list()
    wishlist = await WishlistGinoModel.get(ew_1.id)
    for product in products_149:
        rv = await wishlist.add_product(
            product.id, reserved=False, substitutable=True, product_name=product.name
        )
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
    async def test_product_create(self, snapshot, backend_app, single_user_auth_headers):
        resp = await backend_app.post(
            self.API_URL,
            json={"name": "Product1", "url": "https://devyatkin.dev"},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert "id" in resp_data
        assert "created_at" in resp_data
        assert "updated_at" in resp_data
        resp_data.pop("id", None)
        resp_data.pop("created_at", None)
        resp_data.pop("updated_at", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_products(self, snapshot, backend_app, products_9):
        resp = await backend_app.get(self.API_URL)
        assert resp.status_code == 200
        resp_data = resp.json()
        assert isinstance(resp_data, dict)
        # removing product id from items
        for resp_product in resp_data["items"]:
            assert "id" in resp_product
            assert "created_at" in resp_product
            assert "updated_at" in resp_product
            resp_product.pop("id", None)
            resp_product.pop("created_at", None)
            resp_product.pop("updated_at", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_product_read(self, snapshot, backend_app, products_1):
        resp = await backend_app.get(f"{self.API_URL}/{products_1.id}")
        assert resp.status_code == 200
        resp_data = resp.json()
        assert "id" in resp_data
        assert "created_at" in resp_data
        assert "updated_at" in resp_data
        resp_data.pop("id", None)
        resp_data.pop("created_at", None)
        resp_data.pop("updated_at", None)
        snapshot.assert_match(resp_data)

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
            json={"name": "test-updated", "url": "https://ya.ru"},
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert "id" in resp_data
        assert "created_at" in resp_data
        assert "updated_at" in resp_data
        resp_data.pop("id", None)
        resp_data.pop("created_at", None)
        resp_data.pop("updated_at", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_product_full_update(
        self, snapshot, backend_app, products_1, single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={"name": "test-updated", "url": "https://ya.ru"},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert "id" in resp_data
        assert "created_at" in resp_data
        assert "updated_at" in resp_data
        resp_data.pop("id", None)
        resp_data.pop("created_at", None)
        resp_data.pop("updated_at", None)
        snapshot.assert_match(resp_data)

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
            json={"name": "partial-updated-name"},
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert "id" in resp_data
        assert "created_at" in resp_data
        assert "updated_at" in resp_data
        resp_data.pop("id", None)
        resp_data.pop("created_at", None)
        resp_data.pop("updated_at", None)
        snapshot.assert_match(resp_data)

    async def test_product_partial_update(
        self, snapshot, backend_app, products_1, single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{products_1.id}",
            json={"name": "partial-updated-name"},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert "id" in resp_data
        assert "created_at" in resp_data
        assert "updated_at" in resp_data
        resp_data.pop("id", None)
        resp_data.pop("created_at", None)
        resp_data.pop("updated_at", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_product_paginator_limit(self, snapshot, backend_app, products_9):
        paginator_limit = 5
        resp = await backend_app.get(
            self.API_URL, query_string=dict(size=paginator_limit)
        )
        assert resp.status_code == 200
        resp_json_data = resp.json()
        resp_data = resp_json_data["items"]
        assert len(resp_data) == paginator_limit
        for resp_product in resp_data:
            assert "id" in resp_product
            assert "created_at" in resp_product
            assert "updated_at" in resp_product
            resp_product.pop("id", None)
            resp_product.pop("created_at", None)
            resp_product.pop("updated_at", None)
        snapshot.assert_match(resp_json_data)


class TestEmptyWishlist:
    """Empty wishlist API tests."""

    API_URL = f"{API_URL_PREFIX}/wishlist"

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

    @pytest.mark.api_base
    async def test_empty_wishlist_delete(
        self, backend_app, ew_1, single_user_auth_headers
    ):
        resp = await backend_app.delete(
            f"{self.API_URL}/{ew_1.id}", headers=single_user_auth_headers
        )
        assert resp.status_code == 204

    @pytest.mark.api_base
    async def test_empty_wishlists(self, snapshot, backend_app, empty_wishlists_4):
        resp = await backend_app.get(self.API_URL)
        assert resp.status_code == 200
        resp_json_data = resp.json()
        assert isinstance(resp_json_data, dict)
        items = resp_json_data["items"]
        count = resp_json_data["total"]
        assert count == 4
        # remove unique data from fetch
        for resp_product in items:
            assert "id" in resp_product
            assert "created_at" in resp_product
            assert "updated_at" in resp_product
            resp_product.pop("id", None)
            resp_product.pop("created_at", None)
            resp_product.pop("updated_at", None)
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
        items = resp_data["items"]
        size = resp_data["size"]
        total = resp_data["total"]
        assert size == paginator_limit
        assert total == 4
        # remove unique data from fetch
        for resp_product in items:
            assert "id" in resp_product
            assert "created_at" in resp_product
            assert "updated_at" in resp_product
            resp_product.pop("id", None)
            resp_product.pop("created_at", None)
            resp_product.pop("updated_at", None)
        snapshot.assert_match(items)

    @pytest.mark.api_base
    async def test_empty_wishlist_full_update(
        self, snapshot, backend_app, ew_1, single_user_auth_headers
    ):
        resp = await backend_app.put(
            f"{self.API_URL}/{ew_1.id}",
            json={"name": "test-updated"},
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert "id" in resp_data
        assert "created_at" in resp_data
        assert "updated_at" in resp_data
        resp_data.pop("id", None)
        resp_data.pop("created_at", None)
        resp_data.pop("updated_at", None)
        snapshot.assert_match(resp_data)

    @pytest.mark.api_base
    async def test_empty_wishlist_full_update_no_auth(self, backend_app, ew_1):
        resp = await backend_app.put(
            f"{self.API_URL}/{ew_1.id}", json={"name": "test-updated"}
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
            json={"name": "test-updated"},
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert "id" in resp_data
        assert "created_at" in resp_data
        assert "updated_at" in resp_data
        resp_data.pop("id", None)
        resp_data.pop("created_at", None)
        resp_data.pop("updated_at", None)
        snapshot.assert_match(resp_data)


class TestWishlist:
    """Wishlist API tests."""

    @pytest.mark.api_full
    async def test_delete_wishlist_with_products_no_auth(
        self, backend_app, wishlist_products_1
    ):
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}"
        )
        assert resp.status_code == 401

    @pytest.mark.api_full
    async def test_delete_wishlist_with_products_no_owner(
        self, backend_app, wishlist_products_1, another_single_user_auth_headers
    ):
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}",
            headers=another_single_user_auth_headers,
        )
        assert resp.status_code == 403

    @pytest.mark.api_full
    async def test_delete_wishlist_with_products_admin(
        self, backend_app, wishlist_products_1, single_admin_auth_headers
    ):
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}",
            headers=single_admin_auth_headers,
        )
        assert resp.status_code == 204

    @pytest.mark.api_full
    async def test_delete_wishlist_with_products(
        self, backend_app, wishlist_products_1, single_user_auth_headers
    ):
        resp = await backend_app.delete(
            f"{API_URL_PREFIX}/wishlist/{wishlist_products_1.wishlist_id}",
            headers=single_user_auth_headers,
        )
        assert resp.status_code == 204


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


class TestProductPaginator(PaginatorValidator):
    """Products paginator extra tests."""

    @staticmethod
    def validate_response(json_data: dict):
        response_data = json_data["items"]
        for product in response_data:
            assert "id" in product
            assert "created_at" in product
            assert "updated_at" in product
            product.pop("id", None)
            product.pop("created_at", None)
            product.pop("updated_at", None)
        return json_data

    @pytest.mark.api_full
    async def test_default_paginator(self, snapshot, backend_app, products_149):
        api_url = f"{API_URL_PREFIX}/product"

        # open default page
        response = await backend_app.get(api_url)
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
        response_data = json_data["items"]
        for product in response_data:
            assert "id" in product
            assert "created_at" in product
            assert "updated_at" in product
            product.pop("id", None)
            product.pop("created_at", None)
            product.pop("updated_at", None)
        return json_data

    @pytest.mark.api_full
    async def test_default_paginator(self, snapshot, backend_app, empty_wishlists_149):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open default page
        response = await backend_app.get(api_url)
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
            self_page_num=None,
        )
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_next_page_paginator(self, snapshot, backend_app, empty_wishlists_149):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # open next paginator page
        response = await backend_app.get(api_url, query_string=dict(page=2))
        assert response.status_code == 200
        response_json_data = response.json()
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
    async def test_first_page_paginator(self, snapshot, backend_app, empty_wishlists_149):
        api_url = f"{API_URL_PREFIX}/wishlist"

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
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_last_page_paginator(self, snapshot, backend_app, empty_wishlists_149):
        api_url = f"{API_URL_PREFIX}/wishlist"

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
        snapshot.assert_match(response_json_data)

    @pytest.mark.api_full
    async def test_reduced_qs_paginator(self, snapshot, backend_app, empty_wishlists_149):
        api_url = f"{API_URL_PREFIX}/wishlist"

        # reduce QS size
        response = await backend_app.get(api_url, query_string=dict(size=10))

        assert response.status_code == 200
        response_json_data = response.json()
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
