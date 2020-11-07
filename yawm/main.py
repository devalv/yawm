# -*- coding: utf-8 -*-
"""Project initialization file."""

from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():  # noqa
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):  # noqa
    return {'item_id': item_id, 'q': q}
