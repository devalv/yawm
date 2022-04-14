# -*- coding: utf-8 -*-
"""Utils rest-api handlers."""

from fastapi import APIRouter, Depends

from core.database.models import ProductGinoModel, UserGinoModel
from core.schemas import ExtractUrlInModel, ExtractUrlOutModel
from core.services import get_product_name
from core.services.security import get_current_active_user_by_access_token

utils_router = APIRouter(redirect_slashes=True, tags=["utils"])


@utils_router.post("/extract-product-title", response_model=ExtractUrlOutModel)
async def extract_name_by_url(
    product_url: ExtractUrlInModel,
    current_user: UserGinoModel = Depends(get_current_active_user_by_access_token),
):
    """Extract product name by url."""
    product_with_url = await ProductGinoModel.query.where(
        ProductGinoModel.url == product_url.url
    ).gino.first()

    if product_with_url:
        return {"h1": product_with_url.name}
    value = await get_product_name(product_url.url)
    return {"h1": value}
