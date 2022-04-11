# -*- coding: utf-8 -*-
"""Project database models (Gino)."""

from uuid import uuid4

from fastapi import Depends
from gino.declarative import Model as DeclarativeModel
from gino_starlette import Gino
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core import cached_settings

db = Gino(
    dsn=cached_settings.DATABASE_URI,
    pool_min_size=cached_settings.DB_POOL_MIN_SIZE,
    pool_max_size=cached_settings.DB_POOL_MAX_SIZE,
    echo=cached_settings.DB_ECHO,
    ssl=cached_settings.DB_SSL,
    use_connection_for_request=cached_settings.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=cached_settings.DB_RETRY_LIMIT,
    retry_interval=cached_settings.DB_RETRY_INTERVAL,
)

BaseGinoModel: DeclarativeModel = db.Model


async def get_connection():  # pragma: no cover
    try:
        conn = await db.acquire()
    except:  # noqa
        return False
    else:
        await conn.release()
        return True


def is_database_online(
    db_status: bool = Depends(get_connection),
) -> bool:  # pragma: no cover
    return db_status


class BaseIdModel(BaseGinoModel):
    """Base model reference with id as PK."""

    id = db.Column(UUID(), default=uuid4, primary_key=True)


class BaseCreateDateModel(BaseIdModel):
    """Base model reference with creation auto date."""

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class BaseUpdateDateModel(BaseCreateDateModel):
    """Base model reference with create and update dates + id as a PK."""

    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
