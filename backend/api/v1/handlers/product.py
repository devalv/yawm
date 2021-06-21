# -*- coding: utf-8 -*-
"""Product rest-api handlers."""

from fastapi import APIRouter, Response, status

from fastapi_pagination.ext.gino import paginate

from pydantic import UUID4

from core.database.models.wishlist import Product
from core.schemas import (
    ProductDataCreateModel,
    ProductDataModel,
    ProductDataUpdateModel,
    ProductModel,
)
from core.utils import JsonApiPage

product_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["product"])


@product_router.get("/product", response_model=JsonApiPage[ProductModel])
async def list_products():
    """API for listing all the products."""
    return await paginate(Product.query)


@product_router.get("/product/{id}", response_model=ProductDataModel)
async def get_product(id: UUID4):  # noqa: A002
    """API for getting a product."""
    return await Product.get_or_404(id)


@product_router.post("/product", response_model=ProductDataModel)
async def create_product(product: ProductDataCreateModel):
    """API for creating a new product."""
    return await Product.create(**product.data.validated_attributes)


@product_router.put("/product/{id}", response_model=ProductDataModel)
async def update_product(id: UUID4, product: ProductDataUpdateModel):  # noqa: A002
    """API for updating a product."""
    product_obj = await Product.get_or_404(id)
    await product_obj.update(**product.data.non_null_attributes).apply()
    return product_obj


@product_router.delete(
    "/product/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(id: UUID4):  # noqa: A002
    """API for deleting a product."""
    product = await Product.get_or_404(id)
    await product.delete()
