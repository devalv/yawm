# -*- coding: utf-8 -*-
"""Fastapi-pagination extra utils."""

from __future__ import annotations

from typing import Generic, Sequence, TypeVar

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage, AbstractParams

T = TypeVar("T")


class JsonApiPage(AbstractPage[T], Generic[T]):
    """JSON:API 1.0 specification says that result key should be a `data`."""

    data: Sequence[T]

    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
        cls, items: Sequence[T], total: int, params: AbstractParams
    ) -> JsonApiPage[T]:
        """Same as the original Page.create instead of `data`."""
        return cls(data=items)
