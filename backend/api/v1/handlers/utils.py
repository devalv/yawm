# -*- coding: utf-8 -*-
"""Utils rest-api handlers."""

from fastapi import APIRouter

from core.schemas import (  # noqa: I100
    ExtractUrlDataInModel,
    ExtractUrlModelDataOutModel,
)
from core.services import get_product_name  # noqa: I100

utils_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["utils"])


@utils_router.post("/extract-product-title", response_model=ExtractUrlModelDataOutModel)
async def extract_name_by_url(product_url: ExtractUrlDataInModel):
    """Extract product name by url."""
    # TODO: change status code
    value = await get_product_name(product_url.data.attributes.url)
    return {"data": {"attributes": {"h1": value}}}