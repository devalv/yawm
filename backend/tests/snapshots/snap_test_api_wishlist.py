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

snapshots["TestProduct.test_product_create 1"] = {
    "name": "Product1",
    "price": 123.99,
    "url": "product1",
}

snapshots["TestProduct.test_product_full_update 1"] = {
    "name": "test-updated",
    "price": 12.0,
    "url": "test-url-updated",
}

snapshots["TestProduct.test_product_paginator_limit 1"] = [
    {"name": "test1", "price": 121.31, "url": "test-url1"},
    {"name": "test2", "price": 122.32, "url": "test-url2"},
    {"name": "test3", "price": 123.33, "url": "test-url3"},
    {"name": "test4", "price": 124.34, "url": "test-url4"},
    {"name": "test5", "price": 125.35, "url": "test-url5"},
]

snapshots["TestProduct.test_product_paginator_offset 1"] = [
    {"name": "test6", "price": 126.36, "url": "test-url6"},
    {"name": "test7", "price": 127.37, "url": "test-url7"},
    {"name": "test8", "price": 128.38, "url": "test-url8"},
    {"name": "test9", "price": 129.39, "url": "test-url9"},
]

snapshots["TestProduct.test_product_read 1"] = {
    "name": "test",
    "price": 12.3,
    "url": "test-url",
}

snapshots["TestProduct.test_products 1"] = [
    {"name": "test1", "price": 121.31, "url": "test-url1"},
    {"name": "test2", "price": 122.32, "url": "test-url2"},
    {"name": "test3", "price": 123.33, "url": "test-url3"},
    {"name": "test4", "price": 124.34, "url": "test-url4"},
    {"name": "test5", "price": 125.35, "url": "test-url5"},
    {"name": "test6", "price": 126.36, "url": "test-url6"},
    {"name": "test7", "price": 127.37, "url": "test-url7"},
    {"name": "test8", "price": 128.38, "url": "test-url8"},
    {"name": "test9", "price": 129.39, "url": "test-url9"},
]

snapshots["TestWishlist.test_offset_wishlist_products_list 1"] = [
    {"name": "test6", "price": 126.36, "url": "test-url6"},
    {"name": "test7", "price": 127.37, "url": "test-url7"},
    {"name": "test8", "price": 128.38, "url": "test-url8"},
    {"name": "test9", "price": 129.39, "url": "test-url9"},
]
