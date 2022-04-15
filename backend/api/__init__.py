# -*- coding: utf-8 -*-
"""Project API by versions."""

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi_health import health
from fastapi_pagination import add_pagination
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from core import cached_settings
from core.database import db
from core.health import StatusModel, services_status

from .v1 import product_router as product_router_v1
from .v1 import utils_router as utils_router_v1
from .v1 import wishlist_router as wishlist_router_v1
from .v2 import local_security_router as local_security_router_v2
from .v2 import wishlist_products_router as wishlist_products_router_v2
from .v2 import wishlist_router as wishlist_router_v2


def get_app() -> FastAPI:
    """Just simple application initialization."""
    no_version_app = FastAPI(
        title="Yet another wishlist maker",
        version="0.4.0",
    )
    no_version_app.add_middleware(
        CORSMiddleware,
        allow_origins=list(cached_settings.ALLOW_ORIGINS),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    no_version_app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=[cached_settings.API_DOMAIN]
    )
    no_version_app.add_middleware(GZipMiddleware, minimum_size=500)
    return no_version_app


def configure_routes_v1(application: FastAPI):
    """Configure application."""
    application.include_router(wishlist_router_v1, prefix="/api/v1")
    application.include_router(product_router_v1, prefix="/api/v1")
    application.include_router(utils_router_v1, prefix="/api/v1")
    add_pagination(application)


def configure_routes_v2(application: FastAPI):
    """Configure application routes."""
    application.include_router(wishlist_router_v2, prefix="/api/v2")
    application.include_router(wishlist_products_router_v2, prefix="/api/v2")
    application.include_router(local_security_router_v2, prefix="/api/v2")
    add_pagination(application)


def configure_db(application: FastAPI):
    db.init_app(application)


def configure_health_check(application: FastAPI):
    application.add_api_route(
        "/api/health",
        health([services_status]),
        tags=["service"],
        response_model=StatusModel,
    )


def configure_sentry(application: FastAPI):  # pragma: no cover
    if cached_settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=str(cached_settings.SENTRY_DSN),
            environment=cached_settings.SENTRY_ENVIRONMENT,
        )
        application.add_middleware(SentryAsgiMiddleware)


app = get_app()
configure_routes_v1(application=app)
configure_routes_v2(application=app)
configure_db(app)
configure_health_check(app)
configure_sentry(app)


__all__ = ["app", "db"]
