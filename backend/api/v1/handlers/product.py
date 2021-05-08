# -*- coding: utf-8 -*-
"""Product rest-api handlers."""

import uuid

from fastapi import APIRouter, Response

from fastapi_pagination.ext.gino import paginate

from core.database.models.wishlist import Product  # noqa: I100
from core.schemas import ProductCreateModel, ProductModel, ProductUpdateModel
from core.utils import JsonApiPage  # noqa: I100

product_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["product"])


@product_router.get("/product", response_model=JsonApiPage[ProductModel])
async def list_products():
    """API for listing all the products."""
    return await paginate(Product.query)


@product_router.get("/product/{id}", response_model=ProductModel)
async def get_product(id: uuid.UUID):  # noqa: A002
    """API for getting a product."""
    return await Product.get_or_404(id)


@product_router.post("/product", response_model=ProductModel)
async def create_product(product: ProductCreateModel):
    """API for creating a new product."""
    return await Product.create(**product.validated_attributes)


@product_router.put("/product/{id}", response_model=ProductModel)
async def update_product(id: uuid.UUID, product: ProductUpdateModel):  # noqa: A002
    """API for updating a product."""
    product_obj = await Product.get_or_404(id)
    await product_obj.update(**product.non_null_attributes).apply()
    return product_obj


@product_router.delete("/product/{id}", response_class=Response, status_code=204)
async def delete_product(id: uuid.UUID):  # noqa: A002
    """API for deleting a product."""
    product = await Product.get_or_404(id)
    await product.delete()
