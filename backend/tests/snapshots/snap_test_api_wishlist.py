# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["TestEmptyWishlist.test_empty_wishlist_full_update 1"] = {
    "name": "test-updated",
    "slug": "test-slug-updated",
}

snapshots["TestEmptyWishlist.test_empty_wishlist_read 1"] = {
    "name": "test",
    "slug": "test-slug",
}

snapshots["TestEmptyWishlist.test_empty_wishlists 1"] = [
    {"name": "test1", "slug": "test-slug1"},
    {"name": "test2", "slug": "test-slug2"},
    {"name": "test3", "slug": "test-slug3"},
    {"name": "test4", "slug": "test-slug4"},
]

snapshots["TestEmptyWishlist.test_empty_wishlists_paginator_limit 1"] = [
    {"name": "test1", "slug": "test-slug1"},
    {"name": "test2", "slug": "test-slug2"},
]

snapshots["TestEmptyWishlist.test_empty_wishlists_paginator_offset 1"] = [
    {"name": "test3", "slug": "test-slug3"},
    {"name": "test4", "slug": "test-slug4"},
]

snapshots["TestEmptyWishlist.test_wishlist_create 1"] = {
    "name": "Wishlist1",
    "slug": "wishlist1",
}

snapshots["TestProduct.test_product_create 1"] = {"name": "Product1", "url": "product1"}

snapshots["TestProduct.test_product_full_update 1"] = {
    "name": "test-updated",
    "url": "test-url-updated",
}

snapshots["TestProduct.test_product_paginator_limit 1"] = {
    "items": [
        {"name": "test1"},
        {"name": "test2"},
        {"name": "test3"},
        {"name": "test4"},
        {"name": "test5"},
    ],
    "page": 0,
    "size": 5,
    "total": 9,
}

snapshots["TestProduct.test_product_read 1"] = {"name": "test", "url": "test-url"}

snapshots["TestProduct.test_products 1"] = {
    "items": [
        {"name": "test1"},
        {"name": "test2"},
        {"name": "test3"},
        {"name": "test4"},
        {"name": "test5"},
        {"name": "test6"},
        {"name": "test7"},
        {"name": "test8"},
        {"name": "test9"},
    ],
    "page": 0,
    "size": 50,
    "total": 9,
}

snapshots["TestWishlist.test_offset_wishlist_products_list 1"] = [
    {"name": "test6", "url": "test-url6"},
    {"name": "test7", "url": "test-url7"},
    {"name": "test8", "url": "test-url8"},
    {"name": "test9", "url": "test-url9"},
]
