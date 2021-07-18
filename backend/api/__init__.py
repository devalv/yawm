# -*- coding: utf-8 -*-
"""Project API by versions."""


from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_versioning import VersionedFastAPI

from core.config import SWAP_TOKEN_ENDPOINT
from core.database.models import db

from .v1 import (  # noqa: I201
    product_router,
    security_router,
    utils_router,
    wishlist_product_router,
    wishlist_router,
)


def get_app() -> FastAPI:
    """Just simple application initialization."""
    return FastAPI(
        title="Yet another wishlist maker",
        version="0.2.0",
        swagger_ui_oauth2_redirect_url=SWAP_TOKEN_ENDPOINT,
        swagger_ui_init_oauth={
            "clientId": "please keep this value",
            "clientSecret": "please keep this value",
            "appName": "Yet another wishlist maker",
        },
    )


def configure_routes(application: FastAPI):
    """Configure application."""
    application.include_router(wishlist_router)
    application.include_router(product_router)
    application.include_router(wishlist_product_router)
    application.include_router(utils_router)
    application.include_router(security_router)
    add_pagination(application)


def get_versioned_app(application: FastAPI) -> VersionedFastAPI:
    return VersionedFastAPI(
        application,
        version_format="{major}",
        prefix_format="/api/v{major}",
        swagger_ui_oauth2_redirect_url=SWAP_TOKEN_ENDPOINT,
    )


def configure_db(application: FastAPI):
    db.init_app(application)


app = get_app()
configure_routes(application=app)
app = get_versioned_app(application=app)
configure_db(app)


__all__ = ["app", "db"]
