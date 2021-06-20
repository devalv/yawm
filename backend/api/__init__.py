# -*- coding: utf-8 -*-
"""Project API by versions."""


from fastapi import FastAPI

from fastapi_pagination import add_pagination

from core.config import SWAP_TOKEN_ENDPOINT  # noqa: I100
from core.database.models import db  # noqa: I100
from .v1 import (  # noqa: I201
    product_router,
    security_router,
    utils_router,
    wishlist_product_router,
    wishlist_router,
)


def get_app():
    """Just simple application initialization."""
    application = FastAPI(
        title="Yet another wishlist maker",
        version="0.2.0",
        swagger_ui_oauth2_redirect_url=SWAP_TOKEN_ENDPOINT,
        swagger_ui_init_oauth={
            "clientId": "please keep this value",
            "clientSecret": "please keep this value",
            "appName": "Yet another wishlist maker",
        },
    )
    db.init_app(application)
    return application


def configure(application: FastAPI):
    """Configure application."""
    application.include_router(wishlist_router)
    application.include_router(product_router)
    application.include_router(wishlist_product_router)
    application.include_router(utils_router)
    application.include_router(security_router)


app = get_app()
configure(application=app)
add_pagination(app)

__all__ = ["app", "db"]
