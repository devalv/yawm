# -*- coding: utf-8 -*-
"""Wishlist API V2 tests."""
import uuid

import pytest

from core.database import ProductGinoModel, WishlistGinoModel, WishlistProductsGinoModel

pytestmark = [pytest.mark.asyncio, pytest.mark.api_full]

API_URL_PREFIX = "/api/v2"


@pytest.fixture
async def single_product(single_user):
    return await ProductGinoModel.create(
        user_id=single_user.id, name="test", url="https://devyatkin.dev/1"
    )


@pytest.fixture
async def empty_wishlist(single_user):
    """1 empty wishlist."""
    return await WishlistGinoModel.create(user_id=single_user.id, name="test")


@pytest.fixture
async def wishlist_with_single_product(empty_wishlist, single_product):
    await empty_wishlist.add_product(single_product.id)
    return empty_wishlist


@pytest.fixture
async def wishlist_product(wishlist_with_single_product):
    return await WishlistProductsGinoModel.query.gino.first()


class TestWishlistV2:
    """Wishlist API V2tests."""

    @pytest.mark.api_base
    async def test_create_v2_good(
        self, backend_app, single_user, single_user_auth_headers, single_product
    ):
        handler_url = f"{API_URL_PREFIX}/wishlists"
        test_data = {"product_urls": [{"url": single_product.url}]}
        resp = await backend_app.post(
            handler_url, json=test_data, headers=single_user_auth_headers
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert isinstance(resp_data, dict)
        assert "created_at" in resp_data
        assert "updated_at" in resp_data
        assert "id" in resp_data
        assert "name" in resp_data
        assert resp_data["user_id"] == str(single_user.id)
        assert "products" in resp_data
        response_product = resp_data["products"][0]
        assert "id" in response_product
        assert "created_at" in response_product
        assert "updated_at" in response_product
        assert response_product["name"] == single_product.name
        assert response_product["url"] == single_product.url
        assert response_product["reserved"] is False
        assert response_product["substitutable"] is False

    @pytest.mark.api_base
    async def test_create_v2_no_auth(self, backend_app, single_product):
        handler_url = f"{API_URL_PREFIX}/wishlists"
        test_data = {"product_urls": [{"url": single_product.url}]}
        resp = await backend_app.post(handler_url, json=test_data)
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_create_v2_bad(self, backend_app, single_user_auth_headers):
        handler_url = f"{API_URL_PREFIX}/wishlists"
        test_data = {"product_urls": [{"url": "qwe"}]}
        resp = await backend_app.post(
            handler_url, json=test_data, headers=single_user_auth_headers
        )
        assert resp.status_code == 422

    @pytest.mark.api_base
    async def test_get_v2(self, backend_app, wishlist_with_single_product):
        handler_url = f"{API_URL_PREFIX}/wishlists/{wishlist_with_single_product.id}"
        resp = await backend_app.get(handler_url)
        assert resp.status_code == 200
        resp_data = resp.json()
        assert isinstance(resp_data, dict)
        assert "created_at" in resp_data
        assert "id" in resp_data
        assert "user_id" in resp_data
        assert "products" in resp_data
        assert "updated_at" in resp_data
        assert "name" in resp_data
        response_product = resp_data["products"][0]
        assert "id" in response_product
        assert "created_at" in response_product
        assert "updated_at" in response_product
        assert response_product["name"] == "test"
        assert response_product["url"] == "https://devyatkin.dev/1"
        assert response_product["reserved"] is False
        assert response_product["substitutable"] is False

    @pytest.mark.api_base
    async def test_add_product_good(
        self, backend_app, empty_wishlist, single_user_auth_headers
    ):
        handler_url = f"{API_URL_PREFIX}/wishlists/{empty_wishlist.id}/products-add"
        test_data = {"product_urls": [{"url": "https://devyatkin.dev/1"}]}
        resp = await backend_app.put(
            handler_url, json=test_data, headers=single_user_auth_headers
        )
        assert resp.status_code == 201
        assert len(resp.json()["products"]) == 1

    @pytest.mark.api_base
    async def test_add_product_bad(
        self, backend_app, empty_wishlist, single_user_auth_headers
    ):
        handler_url = f"{API_URL_PREFIX}/wishlists/{empty_wishlist.id}/products-add"
        test_data = {"product_urls": [{"url": "qwe"}]}
        resp = await backend_app.put(
            handler_url, json=test_data, headers=single_user_auth_headers
        )
        assert resp.status_code == 422

    @pytest.mark.api_base
    async def test_add_product_no_auth(self, backend_app, empty_wishlist):
        handler_url = f"{API_URL_PREFIX}/wishlists/{empty_wishlist.id}/products-add"
        test_data = {"product_urls": [{"url": "https://devyatkin.dev/1"}]}
        resp = await backend_app.put(handler_url, json=test_data)
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_reserve_product(self, backend_app, wishlist_product):
        handler_url = f"{API_URL_PREFIX}/wishlist-products/{wishlist_product.id}/reserve"
        resp = await backend_app.put(handler_url)
        assert resp.status_code == 201
        product = await WishlistProductsGinoModel.query.gino.first()
        assert product.reserved is True

    @pytest.mark.api_base
    async def test_delete_product_good(
        self, backend_app, wishlist_product, single_user_auth_headers
    ):
        handler_url = f"{API_URL_PREFIX}/wishlist-products/{wishlist_product.id}"
        resp = await backend_app.delete(handler_url, headers=single_user_auth_headers)
        assert resp.status_code == 204
        product = await WishlistProductsGinoModel.query.gino.first()
        assert product is None

    @pytest.mark.api_base
    async def test_delete_product_bad(
        self, backend_app, wishlist_product, single_user_auth_headers
    ):
        handler_url = f"{API_URL_PREFIX}/wishlist-products/{uuid.uuid4()}"
        resp = await backend_app.delete(handler_url, headers=single_user_auth_headers)
        assert resp.status_code == 404

    @pytest.mark.api_base
    async def test_delete_product_no_auth(self, backend_app, wishlist_product):
        handler_url = f"{API_URL_PREFIX}/wishlist-products/{wishlist_product.id}"
        resp = await backend_app.delete(handler_url)
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_update_product(
        self, backend_app, wishlist_product, single_user_auth_headers
    ):
        handler_url = f"{API_URL_PREFIX}/wishlist-products/{wishlist_product.id}"
        test_data = {"substitutable": True, "reserved": True}
        resp = await backend_app.put(
            handler_url, json=test_data, headers=single_user_auth_headers
        )
        assert resp.status_code == 200
        product = await WishlistProductsGinoModel.query.gino.first()
        assert product.substitutable is True
        assert product.reserved is True

    @pytest.mark.api_base
    async def test_update_product_no_auth(self, backend_app, wishlist_product):
        handler_url = f"{API_URL_PREFIX}/wishlist-products/{wishlist_product.id}"
        test_data = {"substitutable": True, "reserved": True}
        resp = await backend_app.put(handler_url, json=test_data)
        assert resp.status_code == 401

    @pytest.mark.api_base
    async def test_update_product_not_an_owner(
        self, backend_app, wishlist_product, another_single_user_auth_headers
    ):
        handler_url = f"{API_URL_PREFIX}/wishlist-products/{wishlist_product.id}"
        test_data = {"substitutable": True, "reserved": True}
        resp = await backend_app.put(
            handler_url, json=test_data, headers=another_single_user_auth_headers
        )
        assert resp.status_code == 403
