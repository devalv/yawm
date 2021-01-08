# -*- coding: utf-8 -*-
"""Wishlist rest-api handlers."""
import decimal
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Response

from pydantic import BaseModel

from ..models.wishlist import Product, ProductWishlist, Wishlist

wishlist_router = APIRouter(prefix="/api", redirect_slashes=True, tags=["wishlist"])


# TODO: разделить input и output models для очевидности схемы?
# TODO: каскадное удаление
# TODO: статус выполнения операции в ответе?

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


class ProductWishlistModel(BaseModel):
    """ProductWishlist serializer."""

    product_uid: uuid.UUID
    wishlist_uid: uuid.UUID
    uid: Optional[uuid.UUID] = None


# api

# wishlist
@wishlist_router.get("/wishlists", response_model=List[WishlistModel])
async def list_wishlist():
    """API for listing all the wishlists."""
    wishlists = await Wishlist.select("uid", "name", "slug").gino.all()
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


@wishlist_router.delete("/wishlists/{uid}", response_class=Response)
async def delete_wishlist(uid: uuid.UUID):
    """API for deleting a wishlist."""
    wishlist = await Wishlist.get_or_404(uid)
    await wishlist.delete()


@wishlist_router.get("/wishlists/{uid}/products", response_model=List[ProductModel])
async def list_product_wishlists(uid: uuid.UUID):
    """API for getting all related products."""
    wishlist = await Wishlist.get_or_404(uid)
    return await wishlist.get_products()


@wishlist_router.post("/products-wishlist", response_model=ProductWishlistModel)
async def add_product_wishlist(
    product_wishlist: ProductWishlistModel = Depends()  # noqa
):
    """API for adding existing product to a existing wishlist."""
    wishlist = await Wishlist.get_or_404(product_wishlist.wishlist_uid)
    rv = await wishlist.add_product(product_wishlist.product_uid)
    return rv.to_dict()


@wishlist_router.delete("/products-wishlist/{uid}/", response_class=Response)
async def delete_wishlist_product(uid: uuid.UUID):
    """API for removing product from wishlist."""
    product_wishlist = await ProductWishlist.get_or_404(uid)
    await product_wishlist.delete()


# products
@wishlist_router.get("/products", response_model=List[ProductModel])
async def list_products():
    """API for listing all the products."""
    products = await Product.select("uid", "name", "url", "price").gino.all()
    return products


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


@wishlist_router.delete("/products/{uid}", response_class=Response)
async def delete_product(uid: uuid.UUID):
    """API for deleting a product."""
    product = await Product.get_or_404(uid)
    await product.delete()
