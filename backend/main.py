# -*- coding: utf-8 -*-
"""Simple debug application runner."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
