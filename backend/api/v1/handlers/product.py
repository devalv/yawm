# -*- coding: utf-8 -*-
"""Product rest-api handlers."""

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination.ext.gino import paginate
from fastapi_versioning import version

from core.database import ProductGinoModel, UserGinoModel
from core.schemas import (
    ProductDataCreateModel,
    ProductDataModel,
    ProductDataUpdateModel,
    ProductModel,
)
from core.services.security import get_current_user, get_product, get_user_product
from core.utils import JsonApiPage

product_router = APIRouter(redirect_slashes=True, tags=["product"])


@product_router.get("/product", response_model=JsonApiPage[ProductModel])
@version(1)
async def list_products():
    """API for listing all the products."""
    return await paginate(ProductGinoModel.query)


@product_router.get("/product/{id}", response_model=ProductDataModel)
@version(1)
async def get_product(product: ProductGinoModel = Depends(get_product)):  # noqa: B008
    """API for getting a product."""
    return product


@product_router.post("/product", response_model=ProductDataModel)
@version(1)
async def create_product(
    product: ProductDataCreateModel,
    current_user: UserGinoModel = Depends(get_current_user),  # noqa: B008
):
    """API for creating a new product."""
    return await ProductGinoModel.create(
        user_id=current_user.id, **product.data.validated_attributes
    )


@product_router.put("/product/{id}", response_model=ProductDataModel)
@version(1)
async def update_product(
    product_updates: ProductDataUpdateModel,
    product: ProductGinoModel = Depends(get_user_product),  # noqa: B008
):
    """API for updating a product."""
    await product.update(**product_updates.data.non_null_attributes).apply()
    return product


@product_router.delete(
    "/product/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT
)
@version(1)
async def delete_product(
    product: ProductGinoModel = Depends(get_user_product),  # noqa: B008
):
    """API for deleting a product."""
    await product.delete()
