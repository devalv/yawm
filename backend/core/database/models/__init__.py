# -*- coding: utf-8 -*-
"""Project database models (Gino)."""

from uuid import uuid4

from gino_starlette import Gino
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ... import config

db = Gino(
    dsn=config.DB_DSN,
    pool_min_size=config.DB_POOL_MIN_SIZE,
    pool_max_size=config.DB_POOL_MAX_SIZE,
    echo=config.DB_ECHO,
    ssl=config.DB_SSL,
    use_connection_for_request=config.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=config.DB_RETRY_LIMIT,
    retry_interval=config.DB_RETRY_INTERVAL,
)


class AbstractIdModel(db.Model):
    """Abstract model reference with id as PK."""

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A002, A003, VNE003


class AbstractCreateDateModel(AbstractIdModel):
    """Abstract model reference with creation auto date."""

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class AbstractUpdateDateModel(AbstractCreateDateModel):
    """Abstract model reference with create and update dates + id as a PK."""

    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
