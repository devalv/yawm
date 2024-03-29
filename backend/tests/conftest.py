# -*- coding: utf-8 -*-

import pytest_asyncio
from async_asgi_testclient import TestClient

from api import app
from core.database import UserGinoModel


@pytest_asyncio.fixture
def alembic_config():
    return {"script_location": "core/database/migrations"}


@pytest_asyncio.fixture
async def backend_app(alembic_runner):
    """Fixture for async api http tests.

    Each test take new client.
    """
    # upgrade database to a latest alembic migration.
    alembic_runner.managed_upgrade("head")

    async with TestClient(app) as client:
        yield client

    # clear all data in database by downgrade alembic migrations.
    alembic_runner.migrate_down_to("base")


def pytest_sessionfinish(session, exitstatus):
    """Disable exit code 5 if no tests found."""
    if exitstatus == 5:
        session.exitstatus = 0


@pytest_asyncio.fixture
async def user_mock():
    return {
        "disabled": False,
        "superuser": False,
        "username": "test-user",
        "password": "test-user-password",
    }


@pytest_asyncio.fixture
async def another_user_mock():
    return {
        "disabled": False,
        "superuser": False,
        "username": "another-test-user",
        "password": "another-test-user-password",
    }


@pytest_asyncio.fixture
async def disabled_user_mock():
    return {
        "disabled": True,
        "superuser": False,
        "username": "test-user",
        "password": "test-user-password",
    }


@pytest_asyncio.fixture
async def user_admin_mock():
    return {
        "disabled": False,
        "superuser": True,
        "username": "test-user-admin",
        "password": "test-user-admin-password",
    }


@pytest_asyncio.fixture
async def single_admin(backend_app, user_admin_mock):
    return await UserGinoModel.create(**user_admin_mock)


@pytest_asyncio.fixture
async def single_user(backend_app, user_mock):
    return await UserGinoModel.create(**user_mock)


@pytest_asyncio.fixture
async def another_single_user(backend_app, another_user_mock):
    return await UserGinoModel.create(**another_user_mock)


@pytest_asyncio.fixture
async def single_disabled_user(backend_app, disabled_user_mock):
    return await UserGinoModel.create(**disabled_user_mock)


@pytest_asyncio.fixture
async def single_admin_token(single_admin) -> dict:
    return await single_admin.create_token()


@pytest_asyncio.fixture
async def single_user_token(single_user) -> dict:
    return await single_user.create_token()


@pytest_asyncio.fixture
async def another_single_user_token(another_single_user) -> dict:
    return await another_single_user.create_token()


@pytest_asyncio.fixture
async def single_admin_access_token(single_admin_token) -> str:
    return single_admin_token["access_token"]


@pytest_asyncio.fixture
async def single_user_access_token(single_user_token) -> str:
    return single_user_token["access_token"]


@pytest_asyncio.fixture
async def another_single_user_access_token(another_single_user_token) -> str:
    return another_single_user_token["access_token"]


@pytest_asyncio.fixture
async def single_admin_auth_headers(single_admin_access_token) -> dict:
    return {"Authorization": f"Bearer {single_admin_access_token}"}


@pytest_asyncio.fixture
async def single_user_auth_headers(single_user_access_token) -> dict:
    return {"Authorization": f"Bearer {single_user_access_token}"}


@pytest_asyncio.fixture
async def another_single_user_auth_headers(another_single_user_access_token) -> dict:
    return {"Authorization": f"Bearer {another_single_user_access_token}"}
