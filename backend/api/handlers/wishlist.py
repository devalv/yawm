# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""
import decimal
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Response

from pydantic import BaseModel

from fastapi_pagination import Page, LimitOffsetPage
from fastapi_pagination.ext.gino import paginate

from ..models.wishlist import Product, ProductWishlist, Wishlist

wishlist_router = APIRouter(prefix="/api/v1", redirect_slashes=True, tags=["wishlist"])

# TODO: @devalv отдельная модель для редактирования c Optional полями и без id
# TODO: @devalv отдельная модель для создания
# TODO: @devalv отдельная модель для просмотра
# TODO: @devalv каскадное удаление
# TODO: @devalv изменить урлы на более подходящие и универсальные


# pydantic Models aka serializers
class WishlistModel(BaseModel):
    """Wishlist serializer."""

    name: str
    slug: str
    uid: Optional[uuid.UUID] = None


class ProductModel(BaseModel):
    """Product serializer."""

    name: str
    url: str
    price: decimal.Decimal
    uid: Optional[uuid.UUID] = None


class ProductModelOut(BaseModel):
    """Product list serializer."""

    name: str
    uid: uuid.UUID

    class Config:
        orm_mode = True


class ProductWishlistModel(BaseModel):
    """ProductWishlist serializer."""

    product_uid: uuid.UUID
    wishlist_uid: uuid.UUID
    uid: Optional[uuid.UUID] = None
    reserved: Optional[bool]


class ProductWishlistUpdateModel(BaseModel):
    """ProductWishlist update serializer."""

    product_uid: Optional[uuid.UUID]
    wishlist_uid: Optional[uuid.UUID]
    reserved: Optional[bool]


class PaginatorModel(BaseModel):
    """Query paginator serializer."""

    limit: int = 10
    offset: int = 0


# api

# wishlist
@wishlist_router.get("/wishlists", response_model=List[WishlistModel])
async def list_wishlist(paginator: dict = Depends(PaginatorModel)):  # noqa: B008
    """API for listing all the wishlists."""
    wishlists = (
        await Wishlist.select("uid", "name", "slug")
        .limit(paginator.limit)
        .offset(paginator.offset)
        .gino.all()
    )
    return wishlists


@wishlist_router.post("/wishlists", response_model=WishlistModel)
async def add_wishlist(wishlist: WishlistModel):
    """API for creating a new wishlist."""
    rv = await Wishlist.create(name=wishlist.name, slug=wishlist.slug)
    return rv.to_dict()


@wishlist_router.get("/wishlists/{uid}", response_model=WishlistModel)
async def get_wishlist(uid: uuid.UUID):
    """API for getting a wishlist."""
    wishlist = await Wishlist.get_or_404(uid)
    return wishlist.to_dict()


@wishlist_router.delete("/wishlists/{uid}", response_class=Response, status_code=204)
async def delete_wishlist(uid: uuid.UUID):
    """API for deleting a wishlist."""
    wishlist = await Wishlist.get_or_404(uid)
    await wishlist.delete()


@wishlist_router.put("/wishlists/{uid}", response_model=WishlistModel)
async def update_wishlist(uid: uuid.UUID, wishlist: WishlistModel):
    """API for updating a wishlist."""
    wishlist_obj = await Wishlist.get_or_404(uid)
    # remove empty field
    wishlist_dict = {k: v for k, v in wishlist.dict().items() if v is not None}

    await wishlist_obj.update(**wishlist_dict).apply()
    return wishlist_obj.to_dict()


@wishlist_router.get("/wishlists/{uid}/products", response_model=List[ProductModel])
async def list_wishlist_products(
    uid: uuid.UUID, paginator: dict = Depends(PaginatorModel)  # noqa: B008
):
    """API for getting all related products."""
    wishlist = await Wishlist.get_or_404(uid)
    return await wishlist.get_products(
        paginator_limit=paginator.limit, paginator_offset=paginator.offset
    )


@wishlist_router.post("/products-wishlist", response_model=ProductWishlistModel)
async def add_wishlist_product(product_wishlist: ProductWishlistModel):
    """API for adding existing product to a existing wishlist."""
    wishlist = await Wishlist.get_or_404(product_wishlist.wishlist_uid)
    rv = await wishlist.add_product(product_wishlist.product_uid)
    return rv.to_dict()


@wishlist_router.put("/products-wishlist/{uid}", response_model=ProductWishlistModel)
async def reserve_wishlist_product(uid: uuid.UUID, pwm: ProductWishlistUpdateModel):
    """API for reserving existing product-wishlist record."""
    product_wishlist = await ProductWishlist.get_or_404(uid)
    await product_wishlist.update(reserved=pwm.reserved).apply()
    return product_wishlist.to_dict()


@wishlist_router.delete(
    "/products-wishlist/{uid}", response_class=Response, status_code=204
)
async def delete_wishlist_product(uid: uuid.UUID):
    """API for removing product from wishlist."""
    product_wishlist = await ProductWishlist.get_or_404(uid)
    await product_wishlist.delete()


# products
@wishlist_router.get("/products", response_model=Page[ProductModelOut])
@wishlist_router.get(
    "/products/limit-offset", response_model=LimitOffsetPage[ProductModelOut]
)
async def list_products():  # noqa: B008
    """API for listing all the products."""
    products = Product.query
    return await paginate(products)


@wishlist_router.post("/products", response_model=ProductModel)
async def add_product(product: ProductModel):
    """API for creating a new product."""
    rv = await Product.create(name=product.name, url=product.url, price=product.price)
    return rv.to_dict()


@wishlist_router.get("/products/{uid}", response_model=ProductModel)
async def get_product(uid: uuid.UUID):
    """API for getting a product."""
    product = await Product.get_or_404(uid)
    return product.to_dict()


@wishlist_router.delete("/products/{uid}", response_class=Response, status_code=204)
async def delete_product(uid: uuid.UUID):
    """API for deleting a product."""
    product = await Product.get_or_404(uid)
    await product.delete()


@wishlist_router.put("/products/{uid}", response_model=ProductModel)
async def update_product(uid: uuid.UUID, product: ProductModel):
    """API for updating a product."""
    product_obj = await Product.get_or_404(uid)

    # remove empty field
    product_dict = {k: v for k, v in product.dict().items() if v is not None}

    await product_obj.update(**product_dict).apply()
    return product_obj.to_dict()
