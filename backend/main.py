# -*- coding: utf-8 -*-
"""Simple debug application runner."""

from core import config

import uvicorn


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True, host=f"{config.API_HOST}", port=config.API_PORT)
