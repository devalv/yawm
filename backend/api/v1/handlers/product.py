# -*- coding: utf-8 -*-
"""Product rest-api handlers."""

import uuid

from fastapi import APIRouter, Response

from fastapi_pagination.ext.gino import paginate

from core.database.models.wishlist import Product  # noqa: I100
from core.schemas.wishlist import ProductModel, ProductModelList  # noqa: I100
from core.utils import JsonApiPage  # noqa: I100

product_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["product"])


@product_router.get("/products", response_model=JsonApiPage[ProductModelList])
async def list_products():  # noqa: B008
    """API for listing all the products."""
    products = Product.query
    return await paginate(products)


@product_router.post("/products", response_model=ProductModel)
async def add_product(product: ProductModel):
    """API for creating a new product."""
    rv = await Product.create(name=product.name, url=product.url)
    return rv.to_dict()


@product_router.get("/products/{id}", response_model=ProductModel)
async def get_product(id: uuid.UUID):  # noqa: A002
    """API for getting a product."""
    product = await Product.get_or_404(id)
    return product.to_dict()


@product_router.delete("/products/{id}", response_class=Response, status_code=204)
async def delete_product(id: uuid.UUID):  # noqa: A002
    """API for deleting a product."""
    product = await Product.get_or_404(id)
    await product.delete()


@product_router.put("/products/{id}", response_model=ProductModel)
async def update_product(id: uuid.UUID, product: ProductModel):  # noqa: A002
    """API for updating a product."""
    product_obj = await Product.get_or_404(id)

    # remove empty field
    product_dict = {k: v for k, v in product.dict().items() if v is not None}

    await product_obj.update(**product_dict).apply()
    return product_obj.to_dict()
