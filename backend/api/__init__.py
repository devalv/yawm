# -*- coding: utf-8 -*-
"""Yet another wishlist maker."""

from fastapi import FastAPI

from .handlers import wishlist_router
from .models import db


def get_app():
    """Just simple application initialization."""
    application = FastAPI(title="Yet another wishlist maker", version="0.0.1")
    db.init_app(application)
    return application


def configure(application: FastAPI):
    """Configure application."""
    application.include_router(wishlist_router)


app = get_app()
configure(application=app)
