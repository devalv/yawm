# -*- coding: utf-8 -*-
"""Simple debug application runner."""

import uvicorn
from uvicorn.workers import UvicornWorker

from core import cached_settings


class GunicornUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "auto"}


if __name__ == "__main__":
    """For direct run by python -m."""
    uvicorn.run(
        "api:app",
        reload=True,
        host=cached_settings.API_HOST,
        port=cached_settings.API_PORT,
        loop="uvloop",
    )
