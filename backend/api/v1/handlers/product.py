# -*- coding: utf-8 -*-
"""Product rest-api handlers."""

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination.ext.gino import paginate
from fastapi_pagination.links import Page

from core.database import ProductGinoModel, UserGinoModel
from core.schemas import ProductCreateModel, ProductUpdateModel, ProductViewModel
from core.services.security import get_current_user, get_product, get_user_product

product_router = APIRouter(redirect_slashes=True, tags=["product"])


@product_router.get("/product", response_model=Page[ProductViewModel])
async def list_products():
    """API for listing all the products."""
    return await paginate(ProductGinoModel.paginator_query())


@product_router.get("/product/{id}", response_model=ProductViewModel)
async def get_product(product: ProductGinoModel = Depends(get_product)):  # noqa: B008
    """API for getting a product."""
    return product


@product_router.post("/product", response_model=ProductViewModel)
async def create_product(
    product: ProductCreateModel,
    current_user: UserGinoModel = Depends(get_current_user),  # noqa: B008
):
    """API for creating a new product."""
    product_obj = await ProductGinoModel.create(
        user_id=current_user.id, **product.dict()
    )
    return await ProductGinoModel.view_query(product_obj.id)


@product_router.put("/product/{id}", response_model=ProductViewModel)
async def update_product(
    product_updates: ProductUpdateModel,
    product: ProductGinoModel = Depends(get_user_product),  # noqa: B008
):
    """API for updating a product."""
    await product.update(**product_updates.non_null_dict).apply()
    return await ProductGinoModel.view_query(product.id)


@product_router.delete(
    "/product/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
    product: ProductGinoModel = Depends(get_user_product),  # noqa: B008
):
    """API for deleting a product."""
    await product.delete()
