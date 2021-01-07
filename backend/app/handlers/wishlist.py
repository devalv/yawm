# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""
# from typing import Optional
from fastapi import APIRouter

from pydantic import BaseModel

from ..models.wishlist import Product, Wishlist

wishlist_router = APIRouter()


# wishlist
class WishlistModel(BaseModel):
    """Wishlist serializer."""

    name: str
    slug: str


class ProductModel(BaseModel):
    """Product serializer."""

    name: str
    url: str
    price: str
    # TODO: autogenerate unique slug?


class ProductWishlistModel(BaseModel):
    """ProductWishlist serializer."""

    product_id: str
    wishlist_id: str


# TODO: classes
# from fastapi_contrib.pagination import Pagination
# from fastapi_contrib.serializers.common import ModelSerializer
# from fastapi import Depends
#
#
# class WishlistSerializer(ModelSerializer):
#     class Meta:
#         model = Wishlist
#
#
# @wishlist_router.get("/wishlists")
# async def list_wishlist(pagination: Pagination = Depends()):
#     # # TODO: pagination
#     # list = await Wishlist.query.gino.all()
#     # print('list:', list)
#     # return list
#     filter_kwargs = {}
#     return await pagination.paginate(
#         serializer_class=WishlistSerializer, **filter_kwargs
#     )


@wishlist_router.post("/wishlists")
async def add_wishlist(wishlist: WishlistModel):
    """API for creating a new wishlist."""
    rv = await Wishlist.create(name=wishlist.name, slug=wishlist.slug)
    return rv.to_dict()


@wishlist_router.get("/wishlists/{wuid}")
async def get_wishlist(wuid: str):
    """API for getting a wishlist."""
    wishlist = await Wishlist.get_or_404(wuid)
    return wishlist.to_dict()


@wishlist_router.delete("/wishlists/{wuid}")
async def delete_wishlist(wuid: int):
    """API for deleting a wishlist."""
    wishlist = await Wishlist.get_or_404(wuid)
    await wishlist.delete()
    return dict(id=wuid)


@wishlist_router.get("/wishlists")
async def list_wishlist():
    """API for listing all the wishlists."""
    wishlists = await Wishlist.select("id", "name", "slug").gino.all()
    return wishlists


# -----
@wishlist_router.post("/products")
async def add_product(product: ProductModel):
    """API for creating a new product."""
    rv = await Product.create(name=product.name, url=product.url, price=product.price)
    return rv.to_dict()


@wishlist_router.get("/products/{puid}")
async def get_product(puid: str):
    """API for getting a product."""
    product = await Product.get_or_404(puid)
    return product.to_dict()


@wishlist_router.delete("/products/{puid}")
async def delete_product(puid: str):
    """API for deleting a product."""
    product = await Product.get_or_404(puid)
    await product.delete()
    return dict(id=puid)


@wishlist_router.get("/products")
async def list_products():
    """API for listing all the products."""
    products = await Product.select("id", "name", "url", "price").gino.all()
    return products


# -----
@wishlist_router.get("/products-wishlist/{wuid}")
async def list_product_wishlists(wuid: str):
    """API for getting all related products."""
    wishlist = await Wishlist.get_or_404(wuid)
    return await wishlist.get_products()


@wishlist_router.post("/products-wishlist")
async def add_product_wishlist(product_wishlist: ProductWishlistModel):
    """API for adding existing product to a existing wishlist."""
    wishlist = await Wishlist.get_or_404(product_wishlist.wishlist_id)
    rv = await wishlist.add_product(product_wishlist.product_id)
    return rv.to_dict()


@wishlist_router.delete("/products-wishlist/{wuid}-{puid}")
async def delete_wishlist_product(wuid: str, puid: str):
    """API for removing product from wishlist."""
    wishlist = await Wishlist.get_or_404(wuid)
    await wishlist.remove_product(puid)
    return dict(id=wuid)


# ----
@wishlist_router.get("/")
async def root():
    """Empty root page."""
    return dict()
