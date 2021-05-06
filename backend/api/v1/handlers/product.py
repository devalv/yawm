# -*- coding: utf-8 -*-
"""Product rest-api handlers."""

import uuid

from fastapi import APIRouter, Response

from fastapi_pagination import Page
from fastapi_pagination.ext.gino import paginate


from core.database.models.wishlist import Product  # noqa: I100
from core.schemas.wishlist import ProductModel, ProductModelList  # noqa: I100

product_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["product"])


@product_router.get("/products", response_model=Page[ProductModelList])
async def list_products():  # noqa: B008
    """API for listing all the products."""
    products = Product.query
    return await paginate(products)


@product_router.post("/products", response_model=ProductModel)
async def add_product(product: ProductModel):
    """API for creating a new product."""
    rv = await Product.create(name=product.name, url=product.url)
    return rv.to_dict()


@product_router.get("/products/{uid}", response_model=ProductModel)
async def get_product(uid: uuid.UUID):
    """API for getting a product."""
    product = await Product.get_or_404(uid)
    return product.to_dict()


@product_router.delete("/products/{uid}", response_class=Response, status_code=204)
async def delete_product(uid: uuid.UUID):
    """API for deleting a product."""
    product = await Product.get_or_404(uid)
    await product.delete()


@product_router.put("/products/{uid}", response_model=ProductModel)
async def update_product(uid: uuid.UUID, product: ProductModel):
    """API for updating a product."""
    product_obj = await Product.get_or_404(uid)

    # remove empty field
    product_dict = {k: v for k, v in product.dict().items() if v is not None}

    await product_obj.update(**product_dict).apply()
    return product_obj.to_dict()
