# -*- coding: utf-8 -*-
"""ORM Models for Auth entities."""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from jose import jwt
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.config import ACCESS_TOKEN_EXPIRE_MIN, ALGORITHM, SECRET_KEY
from core.utils import CREDENTIALS_EX, JsonApiGinoModel

from .. import db


class User(db.Model, JsonApiGinoModel):
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

    @property
    def id_str(self):
        """Str representation for a self.id."""
        return str(self.id)

    @property
    def active(self):
        return not self.disabled

    def create_access_token(self):
        """Create for a user new access token."""
        token_data = {
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN),
            "id": self.id_str,
            "username": self.username,
        }
        return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    async def insert_or_update_by_ext_id(
        cls,
        sub: str,
        username: str,
        family_name: str = None,
        given_name: str = None,
        full_name: str = None,
        **__
    ) -> User:
        """Create new record or update existing."""

        user_obj = await cls.query.where(cls.ext_id == sub).gino.first()
        if user_obj and user_obj.active:
            await user_obj.update(
                username=username,
                family_name=family_name,
                given_name=given_name,
                full_name=full_name,
            ).apply()
        elif not user_obj:
            user_obj = await cls.create(
                ext_id=sub,
                username=username,
                family_name=family_name,
                given_name=given_name,
                full_name=full_name,
            )
        else:
            raise CREDENTIALS_EX
        return user_obj
