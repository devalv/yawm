# -*- coding: utf-8 -*-
"""Simple debug application runner."""

import uvicorn

from core import config  # noqa: I100


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True, host=f"{config.API_HOST}", port=config.API_PORT)
