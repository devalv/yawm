# -*- coding: utf-8 -*-
"""ORM Models for Auth entities."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core import cached_settings

from .. import BaseUpdateDateModel, db

ref_token_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseUpdateDateModel):
    """Yep, this is a User table."""

    __tablename__ = "user"

    disabled = db.Column(db.Boolean(), nullable=False, default=False)
    superuser = db.Column(db.Boolean(), nullable=False, default=False)
    username = db.Column(db.Unicode(length=255), nullable=False, index=True, unique=True)
    password = db.Column(db.Unicode(length=255), nullable=False)

    @property
    def id_str(self):
        """Str representation for a self.id."""
        return str(self.id)

    @property
    def active(self):
        return not self.disabled

    def create_access_token(self):
        """Create for a user new access token."""
        exp_time: datetime = datetime.utcnow() + timedelta(
            minutes=cached_settings.ACCESS_TOKEN_EXPIRE_MIN
        )
        token_data = {
            "exp": exp_time,
            "id": self.id_str,
            "username": self.username,
        }
        return jwt.encode(
            token_data,
            str(cached_settings.SECRET_KEY),
            algorithm=cached_settings.ALGORITHM,
        )

    async def create_refresh_token(self):
        """Create for a user new refresh token."""
        exp_time: datetime = datetime.utcnow() + timedelta(
            days=cached_settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        token_data = {
            "exp": exp_time,
            "id": self.id_str,
            "username": self.username,
        }
        token = jwt.encode(
            token_data,
            str(cached_settings.SECRET_KEY),
            algorithm=cached_settings.ALGORITHM,
        )
        await TokenInfo.add_token(user_id=self.id, refresh_token=token)
        return token

    async def delete_refresh_token(self):
        """Delete for a user existing refresh token."""
        return await TokenInfo.delete.where(TokenInfo.user_id == self.id).gino.status()

    async def create_token(self) -> Dict[str, Any]:
        acc_token = self.create_access_token()
        ref_token = await self.create_refresh_token()
        return {
            "access_token": acc_token,
            "refresh_token": ref_token,
            "token_type": "bearer",
            "alg": cached_settings.ALGORITHM,
            "typ": "JWT",
        }

    async def token_info(self):
        """Get user existing token information."""
        return await TokenInfo.get(self.id)

    async def token_is_valid(self, token: str) -> bool:
        """Checking that the token matches the issued one."""
        token_info = await self.token_info()
        return bool(token_info and token_info.verify_token(token))

    def verify_password(self, plain_password: str):  # TODO: type
        return pwd_context.verify(plain_password, self.password)

    @staticmethod
    def get_password_hash(password):  # TODO: type
        return pwd_context.hash(password)


class TokenInfo(db.Model):
    """Token information, such as user to whom token was claimed."""

    __tablename__ = "token_info"

    user_id = db.Column(
        UUID(), db.ForeignKey(User.id, ondelete="CASCADE"), primary_key=True
    )
    refresh_token = db.Column(db.Unicode(), nullable=False, index=True)
    created_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    @staticmethod
    def get_refresh_token_hash(token: str):
        """Hash plain token str."""
        return ref_token_context.hash(token)

    @classmethod
    async def add_token(cls, user_id: UUID, refresh_token: str):
        """Add new refresh_token for a user."""
        async with db.transaction():
            await cls.delete.where(cls.user_id == user_id).gino.status()
            await cls.create(
                user_id=user_id, refresh_token=cls.get_refresh_token_hash(refresh_token)
            )

    def verify_token(self, refresh_token: str):
        """Verify plain token text and stored hashed value."""
        return ref_token_context.verify(refresh_token, self.refresh_token)
