# -*- coding: utf-8 -*-
"""PageParser tests."""

from core.services import get_product_name

import pytest
import httpx  # noqa: F401

pytestmark = [pytest.mark.asyncio, pytest.mark.api_full]

API_URL_PREFIX = "/api/v1"


@pytest.fixture
def no_css_response() -> bytes:
    minified_html = b'<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <title>Title</title></head><body><h1>TestProduct1</h1></body></html>'  # noqa: E501
    return minified_html


@pytest.fixture
def css_response() -> bytes:
    minified_html = '<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <title>Title</title></head><body><h1 class="b3a8">adidas Gazelle</h1></body></html>'  # noqa: E501
    return minified_html


@pytest.fixture
def no_h1_response() -> bytes:
    minified_html = '<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <title>Title</title></head><body><h2 class="b3a8">bad</h2></body></html>'  # noqa: E501
    return minified_html


@pytest.fixture
def h3_before_h1_response() -> bytes:
    minified_html = b'<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <title>Title</title></head><body><h3>Fake</h3><h1>TestProduct3</h1></body></html>'  # noqa: E501
    return minified_html


@pytest.fixture
def h11_before_h1_response() -> bytes:
    minified_html = b'<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <title>Title</title></head><body><h11>Fake</h11><h1>TestProduct4</h1></body></html>'  # noqa: E501
    return minified_html


class TestPageParser:
    """Page Parser core tests."""

    async def test_no_css_h1(self, httpx_mock, no_css_response):
        test_url = "https://no_css_h1"
        httpx_mock.add_response(data=no_css_response, url=test_url)

        response = await get_product_name(url=test_url)
        assert response == "TestProduct1"

    async def test_css_h1_one_chunk(self, httpx_mock, css_response):
        test_url = "https://css_h1"
        httpx_mock.add_response(data=css_response, url=test_url)

        response = await get_product_name(url=test_url, chunk_size=500)
        assert response == "adidas Gazelle"

    @pytest.mark.asyncio
    async def test_css_h1_several_chunks(self, httpx_mock, css_response):
        test_url = "https://css_h1"
        httpx_mock.add_response(data=css_response, url=test_url)

        response = await get_product_name(url=test_url, chunk_size=100)
        assert response == "adidas Gazelle"

    @pytest.mark.asyncio
    async def test_no_h1(self, httpx_mock, no_h1_response):
        test_url = "https://no_h1"
        httpx_mock.add_response(data=no_h1_response, url=test_url)

        response = await get_product_name(url=test_url)
        assert response is None

    @pytest.mark.asyncio
    async def test_h3_before_h1(self, httpx_mock, h3_before_h1_response):
        test_url = "https://h3_before_h1"
        httpx_mock.add_response(data=h3_before_h1_response, url=test_url)

        response = await get_product_name(url=test_url)
        assert response == "TestProduct3"

    @pytest.mark.skip(reason="valid spec indicates that headers can only be h1-h6.")
    @pytest.mark.asyncio
    async def test_h11_before_h1(self, httpx_mock, h11_before_h1_response):
        test_url = "https://h11_before_h1"
        httpx_mock.add_response(data=h11_before_h1_response, url=test_url)

        response = await get_product_name(url=test_url)
        assert response == "TestProduct4"

    @pytest.mark.asyncio
    async def test_bad_response(self, httpx_mock):
        test_url = "https://bad"
        httpx_mock.add_response(status_code=500)

        response = await get_product_name(url=test_url)
        assert response is None


class TestApi:
    """PageParser api response tests."""

    API_URL = f"{API_URL_PREFIX}/extract-product-title"

    async def test_bad_input(self, snapshot, api_client):
        resp = await api_client.post(
            f"{self.API_URL}", json={"data": {"attributes": {"url": "bad-url"}}}
        )
        assert resp.status_code == 422
        snapshot.assert_match(resp.json())

    async def test_good_input(self, httpx_mock, snapshot, api_client, css_response):
        test_url = "https://css_h1.io"
        httpx_mock.add_response(data=css_response, url=test_url)

        response = await api_client.post(
            f"{self.API_URL}", json={"data": {"attributes": {"url": test_url}}}
        )
        assert response.status_code == 200
        snapshot.assert_match(response.json())

    async def test_bad_url(self, httpx_mock, snapshot, api_client):
        test_url = "https://bad.io"
        httpx_mock.add_response(status_code=500)

        response = await api_client.post(
            f"{self.API_URL}", json={"data": {"attributes": {"url": test_url}}}
        )
        assert response.status_code == 200
        snapshot.assert_match(response.json())
