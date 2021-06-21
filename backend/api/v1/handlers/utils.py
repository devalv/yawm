# -*- coding: utf-8 -*-
"""Utils rest-api handlers."""

from fastapi import APIRouter

from core.database import ProductGinoModel
from core.schemas import ExtractUrlDataInModel, ExtractUrlModelDataOutModel
from core.services import get_product_name

utils_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["utils"])


@utils_router.post("/extract-product-title", response_model=ExtractUrlModelDataOutModel)
async def extract_name_by_url(product_url: ExtractUrlDataInModel):
    """Extract product name by url."""
    url = product_url.data.attributes.url
    product_with_url = await ProductGinoModel.query.where(
        ProductGinoModel.url == url
    ).gino.first()

    if product_with_url:
        return {"data": {"attributes": {"h1": product_with_url.name}}}
    value = await get_product_name(url)
    return {"data": {"attributes": {"h1": value}}}
