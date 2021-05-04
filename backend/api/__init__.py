# -*- coding: utf-8 -*-
"""Project API by versions."""


from fastapi import FastAPI

from fastapi_pagination import add_pagination

from core.database.models import db  # noqa: I100
from .v1.handlers import wishlist_router  # noqa: I201


def get_app():
    """Just simple application initialization."""
    application = FastAPI(title="Yet another wishlist maker", version="0.0.2")
    db.init_app(application)
    return application


def configure(application: FastAPI):
    """Configure application."""
    application.include_router(wishlist_router)


app = get_app()
configure(application=app)
add_pagination(app)

__all__ = ["app", "db"]
