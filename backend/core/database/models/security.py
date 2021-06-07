# -*- coding: utf-8 -*-
"""ORM Models for Security/Auth entities.

There is no JsonApiGinoModel because of hidden.
"""

from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from . import db


class User(db.Model):
    """Yep, this is a User table."""

    __tablename__ = "user"

    id = db.Column(UUID(), default=uuid4, primary_key=True)  # noqa: A002, A003, VNE003
    ext_id = db.Column(db.Unicode(length=255), nullable=False, unique=True)
    disabled = db.Column(db.Boolean(), nullable=False, default=False)
    superuser = db.Column(db.Boolean(), nullable=False, default=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    username = db.Column(db.Unicode(length=255), nullable=False, index=True)
    given_name = db.Column(db.Unicode(length=255), nullable=True)
    family_name = db.Column(db.Unicode(length=255), nullable=True)
    full_name = db.Column(db.Unicode(length=255), nullable=True)
