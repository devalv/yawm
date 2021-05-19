# -*- coding: utf-8 -*-
"""Fastapi-pagination extra utils."""

from __future__ import annotations

from math import ceil
from typing import Any, Generic, Sequence, TypeVar

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.links.bases import Links, create_links

from pydantic import conint
from pydantic import root_validator


T = TypeVar("T")


class JsonApiPage(AbstractPage[T], Generic[T]):
    """JSON:API 1.0 specification says that result key should be a `data`."""

    total: conint(ge=0)  # type: ignore
    page: conint(ge=0)  # type: ignore
    size: conint(gt=0)  # type: ignore
    data: Sequence[T]
    links: Links

    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
        cls, items: Sequence[T], total: int, params: AbstractParams
    ) -> JsonApiPage[T]:
        """Same as the original Page.create instead of `data`."""
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        return cls(total=total, data=items, page=params.page, size=params.size)

    @root_validator(pre=True)
    def __root_validator__(cls, value: Any) -> Any:
        """Pagination links builder."""
        if "links" not in value:
            page, size, total = [value[k] for k in ("page", "size", "total")]

            value["links"] = create_links(
                first={"page": 0},
                last={"page": ceil(total / size) - 1},
                next={"page": page + 1} if (page + 1) * size < total else None,
                prev={"page": page - 1} if 0 <= page - 1 else None,
            )

        return value
