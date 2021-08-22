# -*- coding: utf-8 -*-
"""Project API by versions."""


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from core.config import SWAP_TOKEN_ENDPOINT
from core.database.models import db

from .v1 import product_router as product_router_v1
from .v1 import security_router as security_router_v1
from .v1 import utils_router as utils_router_v1
from .v1 import wishlist_product_router as wishlist_product_router_v1
from .v1 import wishlist_router as wishlist_router_v1


def get_app() -> FastAPI:
    """Just simple application initialization."""
    no_version_app = FastAPI(
        title="Yet another wishlist maker",
        version="0.2.0",
        swagger_ui_oauth2_redirect_url=SWAP_TOKEN_ENDPOINT,
        swagger_ui_init_oauth={
            "clientId": "please keep this value",
            "clientSecret": "please keep this value",
            "appName": "Yet another wishlist maker",
        },
    )
    no_version_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return no_version_app


def configure_routes_v1(application: FastAPI):
    """Configure application."""
    application.include_router(wishlist_router_v1, prefix="/v1")
    application.include_router(product_router_v1, prefix="/v1")
    application.include_router(wishlist_product_router_v1, prefix="/v1")
    application.include_router(utils_router_v1, prefix="/v1")
    application.include_router(security_router_v1, prefix="/v1")
    add_pagination(application)


def configure_db(application: FastAPI):
    db.init_app(application)


app = get_app()
configure_routes_v1(application=app)
configure_db(app)


__all__ = ["app", "db"]
