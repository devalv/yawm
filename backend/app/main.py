# -*- coding: utf-8 -*-
"""Project initialization file."""

from typing import Optional

from fastapi import FastAPI

from .models import db
# from .models.test import User


def get_app():
    application = FastAPI(title="Yet another wishlist maker", version="0.0.1")
    db.init_app(application)
    return application


app = get_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/items/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):  # noqa
    return {'item_id': item_id, 'q': q}

