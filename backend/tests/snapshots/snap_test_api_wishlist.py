# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["TestEmptyWishlist.test_empty_wishlist_full_update 1"] = {
    "name": "test-updated"
}

snapshots["TestEmptyWishlist.test_empty_wishlist_read 1"] = {"name": "test"}

snapshots["TestEmptyWishlist.test_empty_wishlists 1"] = [
    {"name": "test1"},
    {"name": "test2"},
    {"name": "test3"},
    {"name": "test4"},
]

snapshots["TestEmptyWishlist.test_empty_wishlists_paginator_limit 1"] = [
    {"name": "test1"},
    {"name": "test2"},
]

snapshots["TestEmptyWishlist.test_wishlist_create 1"] = {"name": "Wishlist1"}

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
