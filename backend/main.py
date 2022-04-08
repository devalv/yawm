# -*- coding: utf-8 -*-
"""Simple debug application runner."""

import uvicorn
from uvicorn.workers import UvicornWorker

from core import config


class GunicornUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "auto"}


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        reload=True,
        host=config.API_HOST,
        port=config.API_PORT,
        loop="uvloop",
    )
