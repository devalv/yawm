# -*- coding: utf-8 -*-
"""Project configuration file (Starlette)."""

from sqlalchemy.engine.url import URL, make_url

from starlette.config import Config
from starlette.datastructures import Secret


config = Config(".env")
# Gino
DB_DRIVER = config("DB_DRIVER", default="postgresql")
DB_HOST = config("DB_HOST", default=None)
DB_PORT = config("DB_PORT", cast=int, default=None)
DB_USER = config("DB_USER", cast=str, default=None)
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default=None)
DB_DATABASE = config("DB_DATABASE", default=None)
DB_DSN = config(
    "DB_DSN",
    cast=make_url,
    default=URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
    ),
)
DB_POOL_MIN_SIZE = config("DB_POOL_MIN_SIZE", cast=int, default=1)
DB_POOL_MAX_SIZE = config("DB_POOL_MAX_SIZE", cast=int, default=16)
DB_ECHO = config("DB_ECHO", cast=bool, default=False)
DB_SSL = config("DB_SSL", default=None)
DB_USE_CONNECTION_FOR_REQUEST = config(
    "DB_USE_CONNECTION_FOR_REQUEST", cast=bool, default=True
)
DB_RETRY_LIMIT = config("DB_RETRY_LIMIT", cast=int, default=1)
DB_RETRY_INTERVAL = config("DB_RETRY_INTERVAL", cast=int, default=1)
# uvicorn
API_HOST = config("API_HOST", default="127.0.0.1")
API_PORT = config("API_PORT", cast=int, default=8000)
# security
API_DOMAIN = config("API_DOMAIN", default=None)
SECRET_KEY = config("SECRET_KEY", default=None)
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MIN = config("ACCESS_TOKEN_EXPIRE_MIN", default=30)
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID", default=None)
GOOGLE_CLIENT_SECRETS_JSON = config("GOOGLE_CLIENT_SECRETS_JSON", default=None)
# crawler User-Agent
CRAWLER_USER_AGENT = config("CRAWLER_USER_AGENT", default="yawm-api")
