# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["TestProduct.test_product_create 1"] = {
    "name": "Product1",
    "price": 123.99,
    "url": "product1",
}

snapshots["TestProduct.test_product_read 1"] = {
    "name": "test",
    "price": 12.3,
    "url": "test-url",
}

snapshots["TestProduct.test_product_update 1"] = {
    "name": "test-updated",
    "price": 12.0,
    "url": "test-url-updated",
}

snapshots["TestProduct.test_products 1"] = [
    {"name": "Product1", "price": 123.99, "url": "product1"},
    {"name": "test", "price": 123.32, "url": "test-url"},
]
