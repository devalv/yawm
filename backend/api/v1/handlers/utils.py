# -*- coding: utf-8 -*-
"""Utils rest-api handlers."""

from fastapi import APIRouter, status

from core.schemas import (  # noqa: I100
    ExtractUrlDataInModel,
    ExtractUrlModelDataOutModel,
)

utils_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["utils"])


@utils_router.post(
    "/extract-product-title",
    response_model=ExtractUrlModelDataOutModel,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
async def extract_name_by_url(product_url: ExtractUrlDataInModel):
    """Extract product name by url."""
    # TODO: provide code
    h1_str = f"h1 header of {product_url.data.attributes.url}"
    title_str = f"title of {product_url.data.attributes.url}"
    return {"data": {"attributes": {"h1": h1_str, "title": title_str}}}
