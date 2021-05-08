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
    {"attributes": {"name": "test1"}, "type": "wishlist"},
    {"attributes": {"name": "test2"}, "type": "wishlist"},
    {"attributes": {"name": "test3"}, "type": "wishlist"},
    {"attributes": {"name": "test4"}, "type": "wishlist"},
]

snapshots["TestEmptyWishlist.test_empty_wishlists_paginator_limit 1"] = [
    {"attributes": {"name": "test1"}, "type": "wishlist"},
    {"attributes": {"name": "test2"}, "type": "wishlist"},
]

snapshots["TestEmptyWishlist.test_wishlist_create 1"] = {"name": "Wishlist1"}

snapshots["TestProduct.test_product_create 1"] = {
    "attributes": {"name": "Product1", "url": "https://devyatkin.dev"},
    "type": "product",
}

snapshots["TestProduct.test_product_full_update 1"] = {
    "attributes": {"name": "test-updated", "url": "https://ya.ru"},
    "type": "product",
}

snapshots["TestProduct.test_product_paginator_limit 1"] = {
    "data": [
        {
            "attributes": {"name": "test1", "url": "https://devyatkin.dev/1"},
            "type": "product",
        },
        {
            "attributes": {"name": "test2", "url": "https://devyatkin.dev/2"},
            "type": "product",
        },
        {
            "attributes": {"name": "test3", "url": "https://devyatkin.dev/3"},
            "type": "product",
        },
        {
            "attributes": {"name": "test4", "url": "https://devyatkin.dev/4"},
            "type": "product",
        },
        {
            "attributes": {"name": "test5", "url": "https://devyatkin.dev/5"},
            "type": "product",
        },
    ],
    "page": 0,
    "size": 5,
    "total": 9,
}

snapshots["TestProduct.test_product_partial_update 1"] = {
    "attributes": {"name": "partial-updated-name", "url": "https://devyatkin.dev/1"},
    "type": "product",
}

snapshots["TestProduct.test_product_read 1"] = {
    "attributes": {"name": "test", "url": "https://devyatkin.dev/1"},
    "type": "product",
}

snapshots["TestProduct.test_products 1"] = {
    "data": [
        {
            "attributes": {"name": "test1", "url": "https://devyatkin.dev/1"},
            "type": "product",
        },
        {
            "attributes": {"name": "test2", "url": "https://devyatkin.dev/2"},
            "type": "product",
        },
        {
            "attributes": {"name": "test3", "url": "https://devyatkin.dev/3"},
            "type": "product",
        },
        {
            "attributes": {"name": "test4", "url": "https://devyatkin.dev/4"},
            "type": "product",
        },
        {
            "attributes": {"name": "test5", "url": "https://devyatkin.dev/5"},
            "type": "product",
        },
        {
            "attributes": {"name": "test6", "url": "https://devyatkin.dev/6"},
            "type": "product",
        },
        {
            "attributes": {"name": "test7", "url": "https://devyatkin.dev/7"},
            "type": "product",
        },
        {
            "attributes": {"name": "test8", "url": "https://devyatkin.dev/8"},
            "type": "product",
        },
        {
            "attributes": {"name": "test9", "url": "https://devyatkin.dev/9"},
            "type": "product",
        },
    ],
    "page": 0,
    "size": 50,
    "total": 9,
}
