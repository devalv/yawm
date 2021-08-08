# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["TestEmptyWishlist.test_empty_wishlist_full_update 1"] = {
    "attributes": {"name": "test-updated"},
    "type": "wishlist",
}

snapshots["TestEmptyWishlist.test_empty_wishlist_full_update_admin 1"] = {
    "attributes": {"name": "test-updated"},
    "type": "wishlist",
}

snapshots["TestEmptyWishlist.test_empty_wishlist_read 1"] = {
    "attributes": {"name": "test"},
    "type": "wishlist",
}

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

snapshots["TestEmptyWishlist.test_wishlist_create 1"] = {
    "data": {"attributes": {"name": "Wishlist1"}, "type": "wishlist"}
}

snapshots["TestProduct.test_product_create 1"] = {
    "data": {
        "attributes": {"name": "Product1", "url": "https://devyatkin.dev"},
        "type": "product",
    }
}

snapshots["TestProduct.test_product_full_update 1"] = {
    "data": {
        "attributes": {"name": "test-updated", "url": "https://ya.ru"},
        "type": "product",
    }
}

snapshots["TestProduct.test_product_full_update_admin 1"] = {
    "data": {
        "attributes": {"name": "test-updated", "url": "https://ya.ru"},
        "type": "product",
    }
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
    "links": {
        "first": "/v1/product?size=5&page=1",
        "last": "/v1/product?size=5&page=2",
        "next": "/v1/product?size=5&page=2",
        "prev": None,
        "self": "/v1/product?size=5",
    },
    "page": 1,
    "size": 5,
    "total": 9,
}

snapshots["TestProduct.test_product_partial_update 1"] = {
    "data": {
        "attributes": {
            "name": "partial-updated-name",
            "url": "https://devyatkin.dev/1",
        },
        "type": "product",
    }
}

snapshots["TestProduct.test_product_partial_update_admin 1"] = {
    "data": {
        "attributes": {
            "name": "partial-updated-name",
            "url": "https://devyatkin.dev/1",
        },
        "type": "product",
    }
}

snapshots["TestProduct.test_product_read 1"] = {
    "data": {
        "attributes": {"name": "test", "url": "https://devyatkin.dev/1"},
        "type": "product",
    }
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
    "links": {
        "first": "/v1/product?page=1",
        "last": "/v1/product?page=1",
        "next": None,
        "prev": None,
        "self": "/v1/product",
    },
    "page": 1,
    "size": 50,
    "total": 9,
}

snapshots["TestProductPaginator.test_default_paginator 1"] = {
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
        {
            "attributes": {"name": "test10", "url": "https://devyatkin.dev/10"},
            "type": "product",
        },
        {
            "attributes": {"name": "test11", "url": "https://devyatkin.dev/11"},
            "type": "product",
        },
        {
            "attributes": {"name": "test12", "url": "https://devyatkin.dev/12"},
            "type": "product",
        },
        {
            "attributes": {"name": "test13", "url": "https://devyatkin.dev/13"},
            "type": "product",
        },
        {
            "attributes": {"name": "test14", "url": "https://devyatkin.dev/14"},
            "type": "product",
        },
        {
            "attributes": {"name": "test15", "url": "https://devyatkin.dev/15"},
            "type": "product",
        },
        {
            "attributes": {"name": "test16", "url": "https://devyatkin.dev/16"},
            "type": "product",
        },
        {
            "attributes": {"name": "test17", "url": "https://devyatkin.dev/17"},
            "type": "product",
        },
        {
            "attributes": {"name": "test18", "url": "https://devyatkin.dev/18"},
            "type": "product",
        },
        {
            "attributes": {"name": "test19", "url": "https://devyatkin.dev/19"},
            "type": "product",
        },
        {
            "attributes": {"name": "test20", "url": "https://devyatkin.dev/20"},
            "type": "product",
        },
        {
            "attributes": {"name": "test21", "url": "https://devyatkin.dev/21"},
            "type": "product",
        },
        {
            "attributes": {"name": "test22", "url": "https://devyatkin.dev/22"},
            "type": "product",
        },
        {
            "attributes": {"name": "test23", "url": "https://devyatkin.dev/23"},
            "type": "product",
        },
        {
            "attributes": {"name": "test24", "url": "https://devyatkin.dev/24"},
            "type": "product",
        },
        {
            "attributes": {"name": "test25", "url": "https://devyatkin.dev/25"},
            "type": "product",
        },
        {
            "attributes": {"name": "test26", "url": "https://devyatkin.dev/26"},
            "type": "product",
        },
        {
            "attributes": {"name": "test27", "url": "https://devyatkin.dev/27"},
            "type": "product",
        },
        {
            "attributes": {"name": "test28", "url": "https://devyatkin.dev/28"},
            "type": "product",
        },
        {
            "attributes": {"name": "test29", "url": "https://devyatkin.dev/29"},
            "type": "product",
        },
        {
            "attributes": {"name": "test30", "url": "https://devyatkin.dev/30"},
            "type": "product",
        },
        {
            "attributes": {"name": "test31", "url": "https://devyatkin.dev/31"},
            "type": "product",
        },
        {
            "attributes": {"name": "test32", "url": "https://devyatkin.dev/32"},
            "type": "product",
        },
        {
            "attributes": {"name": "test33", "url": "https://devyatkin.dev/33"},
            "type": "product",
        },
        {
            "attributes": {"name": "test34", "url": "https://devyatkin.dev/34"},
            "type": "product",
        },
        {
            "attributes": {"name": "test35", "url": "https://devyatkin.dev/35"},
            "type": "product",
        },
        {
            "attributes": {"name": "test36", "url": "https://devyatkin.dev/36"},
            "type": "product",
        },
        {
            "attributes": {"name": "test37", "url": "https://devyatkin.dev/37"},
            "type": "product",
        },
        {
            "attributes": {"name": "test38", "url": "https://devyatkin.dev/38"},
            "type": "product",
        },
        {
            "attributes": {"name": "test39", "url": "https://devyatkin.dev/39"},
            "type": "product",
        },
        {
            "attributes": {"name": "test40", "url": "https://devyatkin.dev/40"},
            "type": "product",
        },
        {
            "attributes": {"name": "test41", "url": "https://devyatkin.dev/41"},
            "type": "product",
        },
        {
            "attributes": {"name": "test42", "url": "https://devyatkin.dev/42"},
            "type": "product",
        },
        {
            "attributes": {"name": "test43", "url": "https://devyatkin.dev/43"},
            "type": "product",
        },
        {
            "attributes": {"name": "test44", "url": "https://devyatkin.dev/44"},
            "type": "product",
        },
        {
            "attributes": {"name": "test45", "url": "https://devyatkin.dev/45"},
            "type": "product",
        },
        {
            "attributes": {"name": "test46", "url": "https://devyatkin.dev/46"},
            "type": "product",
        },
        {
            "attributes": {"name": "test47", "url": "https://devyatkin.dev/47"},
            "type": "product",
        },
        {
            "attributes": {"name": "test48", "url": "https://devyatkin.dev/48"},
            "type": "product",
        },
        {
            "attributes": {"name": "test49", "url": "https://devyatkin.dev/49"},
            "type": "product",
        },
        {
            "attributes": {"name": "test50", "url": "https://devyatkin.dev/50"},
            "type": "product",
        },
    ],
    "page": 1,
    "size": 50,
    "total": 149,
}

snapshots["TestProductPaginator.test_empty_page_reduced_qs_paginator 1"] = {
    "data": [],
    "page": 16,
    "size": 10,
    "total": 149,
}

snapshots["TestProductPaginator.test_first_page_paginator 1"] = {
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
        {
            "attributes": {"name": "test10", "url": "https://devyatkin.dev/10"},
            "type": "product",
        },
        {
            "attributes": {"name": "test11", "url": "https://devyatkin.dev/11"},
            "type": "product",
        },
        {
            "attributes": {"name": "test12", "url": "https://devyatkin.dev/12"},
            "type": "product",
        },
        {
            "attributes": {"name": "test13", "url": "https://devyatkin.dev/13"},
            "type": "product",
        },
        {
            "attributes": {"name": "test14", "url": "https://devyatkin.dev/14"},
            "type": "product",
        },
        {
            "attributes": {"name": "test15", "url": "https://devyatkin.dev/15"},
            "type": "product",
        },
        {
            "attributes": {"name": "test16", "url": "https://devyatkin.dev/16"},
            "type": "product",
        },
        {
            "attributes": {"name": "test17", "url": "https://devyatkin.dev/17"},
            "type": "product",
        },
        {
            "attributes": {"name": "test18", "url": "https://devyatkin.dev/18"},
            "type": "product",
        },
        {
            "attributes": {"name": "test19", "url": "https://devyatkin.dev/19"},
            "type": "product",
        },
        {
            "attributes": {"name": "test20", "url": "https://devyatkin.dev/20"},
            "type": "product",
        },
        {
            "attributes": {"name": "test21", "url": "https://devyatkin.dev/21"},
            "type": "product",
        },
        {
            "attributes": {"name": "test22", "url": "https://devyatkin.dev/22"},
            "type": "product",
        },
        {
            "attributes": {"name": "test23", "url": "https://devyatkin.dev/23"},
            "type": "product",
        },
        {
            "attributes": {"name": "test24", "url": "https://devyatkin.dev/24"},
            "type": "product",
        },
        {
            "attributes": {"name": "test25", "url": "https://devyatkin.dev/25"},
            "type": "product",
        },
        {
            "attributes": {"name": "test26", "url": "https://devyatkin.dev/26"},
            "type": "product",
        },
        {
            "attributes": {"name": "test27", "url": "https://devyatkin.dev/27"},
            "type": "product",
        },
        {
            "attributes": {"name": "test28", "url": "https://devyatkin.dev/28"},
            "type": "product",
        },
        {
            "attributes": {"name": "test29", "url": "https://devyatkin.dev/29"},
            "type": "product",
        },
        {
            "attributes": {"name": "test30", "url": "https://devyatkin.dev/30"},
            "type": "product",
        },
        {
            "attributes": {"name": "test31", "url": "https://devyatkin.dev/31"},
            "type": "product",
        },
        {
            "attributes": {"name": "test32", "url": "https://devyatkin.dev/32"},
            "type": "product",
        },
        {
            "attributes": {"name": "test33", "url": "https://devyatkin.dev/33"},
            "type": "product",
        },
        {
            "attributes": {"name": "test34", "url": "https://devyatkin.dev/34"},
            "type": "product",
        },
        {
            "attributes": {"name": "test35", "url": "https://devyatkin.dev/35"},
            "type": "product",
        },
        {
            "attributes": {"name": "test36", "url": "https://devyatkin.dev/36"},
            "type": "product",
        },
        {
            "attributes": {"name": "test37", "url": "https://devyatkin.dev/37"},
            "type": "product",
        },
        {
            "attributes": {"name": "test38", "url": "https://devyatkin.dev/38"},
            "type": "product",
        },
        {
            "attributes": {"name": "test39", "url": "https://devyatkin.dev/39"},
            "type": "product",
        },
        {
            "attributes": {"name": "test40", "url": "https://devyatkin.dev/40"},
            "type": "product",
        },
        {
            "attributes": {"name": "test41", "url": "https://devyatkin.dev/41"},
            "type": "product",
        },
        {
            "attributes": {"name": "test42", "url": "https://devyatkin.dev/42"},
            "type": "product",
        },
        {
            "attributes": {"name": "test43", "url": "https://devyatkin.dev/43"},
            "type": "product",
        },
        {
            "attributes": {"name": "test44", "url": "https://devyatkin.dev/44"},
            "type": "product",
        },
        {
            "attributes": {"name": "test45", "url": "https://devyatkin.dev/45"},
            "type": "product",
        },
        {
            "attributes": {"name": "test46", "url": "https://devyatkin.dev/46"},
            "type": "product",
        },
        {
            "attributes": {"name": "test47", "url": "https://devyatkin.dev/47"},
            "type": "product",
        },
        {
            "attributes": {"name": "test48", "url": "https://devyatkin.dev/48"},
            "type": "product",
        },
        {
            "attributes": {"name": "test49", "url": "https://devyatkin.dev/49"},
            "type": "product",
        },
        {
            "attributes": {"name": "test50", "url": "https://devyatkin.dev/50"},
            "type": "product",
        },
    ],
    "page": 1,
    "size": 50,
    "total": 149,
}

snapshots["TestProductPaginator.test_last_page_paginator 1"] = {
    "data": [
        {
            "attributes": {"name": "test101", "url": "https://devyatkin.dev/101"},
            "type": "product",
        },
        {
            "attributes": {"name": "test102", "url": "https://devyatkin.dev/102"},
            "type": "product",
        },
        {
            "attributes": {"name": "test103", "url": "https://devyatkin.dev/103"},
            "type": "product",
        },
        {
            "attributes": {"name": "test104", "url": "https://devyatkin.dev/104"},
            "type": "product",
        },
        {
            "attributes": {"name": "test105", "url": "https://devyatkin.dev/105"},
            "type": "product",
        },
        {
            "attributes": {"name": "test106", "url": "https://devyatkin.dev/106"},
            "type": "product",
        },
        {
            "attributes": {"name": "test107", "url": "https://devyatkin.dev/107"},
            "type": "product",
        },
        {
            "attributes": {"name": "test108", "url": "https://devyatkin.dev/108"},
            "type": "product",
        },
        {
            "attributes": {"name": "test109", "url": "https://devyatkin.dev/109"},
            "type": "product",
        },
        {
            "attributes": {"name": "test110", "url": "https://devyatkin.dev/110"},
            "type": "product",
        },
        {
            "attributes": {"name": "test111", "url": "https://devyatkin.dev/111"},
            "type": "product",
        },
        {
            "attributes": {"name": "test112", "url": "https://devyatkin.dev/112"},
            "type": "product",
        },
        {
            "attributes": {"name": "test113", "url": "https://devyatkin.dev/113"},
            "type": "product",
        },
        {
            "attributes": {"name": "test114", "url": "https://devyatkin.dev/114"},
            "type": "product",
        },
        {
            "attributes": {"name": "test115", "url": "https://devyatkin.dev/115"},
            "type": "product",
        },
        {
            "attributes": {"name": "test116", "url": "https://devyatkin.dev/116"},
            "type": "product",
        },
        {
            "attributes": {"name": "test117", "url": "https://devyatkin.dev/117"},
            "type": "product",
        },
        {
            "attributes": {"name": "test118", "url": "https://devyatkin.dev/118"},
            "type": "product",
        },
        {
            "attributes": {"name": "test119", "url": "https://devyatkin.dev/119"},
            "type": "product",
        },
        {
            "attributes": {"name": "test120", "url": "https://devyatkin.dev/120"},
            "type": "product",
        },
        {
            "attributes": {"name": "test121", "url": "https://devyatkin.dev/121"},
            "type": "product",
        },
        {
            "attributes": {"name": "test122", "url": "https://devyatkin.dev/122"},
            "type": "product",
        },
        {
            "attributes": {"name": "test123", "url": "https://devyatkin.dev/123"},
            "type": "product",
        },
        {
            "attributes": {"name": "test124", "url": "https://devyatkin.dev/124"},
            "type": "product",
        },
        {
            "attributes": {"name": "test125", "url": "https://devyatkin.dev/125"},
            "type": "product",
        },
        {
            "attributes": {"name": "test126", "url": "https://devyatkin.dev/126"},
            "type": "product",
        },
        {
            "attributes": {"name": "test127", "url": "https://devyatkin.dev/127"},
            "type": "product",
        },
        {
            "attributes": {"name": "test128", "url": "https://devyatkin.dev/128"},
            "type": "product",
        },
        {
            "attributes": {"name": "test129", "url": "https://devyatkin.dev/129"},
            "type": "product",
        },
        {
            "attributes": {"name": "test130", "url": "https://devyatkin.dev/130"},
            "type": "product",
        },
        {
            "attributes": {"name": "test131", "url": "https://devyatkin.dev/131"},
            "type": "product",
        },
        {
            "attributes": {"name": "test132", "url": "https://devyatkin.dev/132"},
            "type": "product",
        },
        {
            "attributes": {"name": "test133", "url": "https://devyatkin.dev/133"},
            "type": "product",
        },
        {
            "attributes": {"name": "test134", "url": "https://devyatkin.dev/134"},
            "type": "product",
        },
        {
            "attributes": {"name": "test135", "url": "https://devyatkin.dev/135"},
            "type": "product",
        },
        {
            "attributes": {"name": "test136", "url": "https://devyatkin.dev/136"},
            "type": "product",
        },
        {
            "attributes": {"name": "test137", "url": "https://devyatkin.dev/137"},
            "type": "product",
        },
        {
            "attributes": {"name": "test138", "url": "https://devyatkin.dev/138"},
            "type": "product",
        },
        {
            "attributes": {"name": "test139", "url": "https://devyatkin.dev/139"},
            "type": "product",
        },
        {
            "attributes": {"name": "test140", "url": "https://devyatkin.dev/140"},
            "type": "product",
        },
        {
            "attributes": {"name": "test141", "url": "https://devyatkin.dev/141"},
            "type": "product",
        },
        {
            "attributes": {"name": "test142", "url": "https://devyatkin.dev/142"},
            "type": "product",
        },
        {
            "attributes": {"name": "test143", "url": "https://devyatkin.dev/143"},
            "type": "product",
        },
        {
            "attributes": {"name": "test144", "url": "https://devyatkin.dev/144"},
            "type": "product",
        },
        {
            "attributes": {"name": "test145", "url": "https://devyatkin.dev/145"},
            "type": "product",
        },
        {
            "attributes": {"name": "test146", "url": "https://devyatkin.dev/146"},
            "type": "product",
        },
        {
            "attributes": {"name": "test147", "url": "https://devyatkin.dev/147"},
            "type": "product",
        },
        {
            "attributes": {"name": "test148", "url": "https://devyatkin.dev/148"},
            "type": "product",
        },
        {
            "attributes": {"name": "test149", "url": "https://devyatkin.dev/149"},
            "type": "product",
        },
    ],
    "page": 3,
    "size": 50,
    "total": 149,
}

snapshots["TestProductPaginator.test_last_page_reduced_qs_paginator 1"] = {
    "data": [
        {
            "attributes": {"name": "test141", "url": "https://devyatkin.dev/141"},
            "type": "product",
        },
        {
            "attributes": {"name": "test142", "url": "https://devyatkin.dev/142"},
            "type": "product",
        },
        {
            "attributes": {"name": "test143", "url": "https://devyatkin.dev/143"},
            "type": "product",
        },
        {
            "attributes": {"name": "test144", "url": "https://devyatkin.dev/144"},
            "type": "product",
        },
        {
            "attributes": {"name": "test145", "url": "https://devyatkin.dev/145"},
            "type": "product",
        },
        {
            "attributes": {"name": "test146", "url": "https://devyatkin.dev/146"},
            "type": "product",
        },
        {
            "attributes": {"name": "test147", "url": "https://devyatkin.dev/147"},
            "type": "product",
        },
        {
            "attributes": {"name": "test148", "url": "https://devyatkin.dev/148"},
            "type": "product",
        },
        {
            "attributes": {"name": "test149", "url": "https://devyatkin.dev/149"},
            "type": "product",
        },
    ],
    "page": 15,
    "size": 10,
    "total": 149,
}

snapshots["TestProductPaginator.test_next_page_paginator 1"] = {
    "data": [
        {
            "attributes": {"name": "test51", "url": "https://devyatkin.dev/51"},
            "type": "product",
        },
        {
            "attributes": {"name": "test52", "url": "https://devyatkin.dev/52"},
            "type": "product",
        },
        {
            "attributes": {"name": "test53", "url": "https://devyatkin.dev/53"},
            "type": "product",
        },
        {
            "attributes": {"name": "test54", "url": "https://devyatkin.dev/54"},
            "type": "product",
        },
        {
            "attributes": {"name": "test55", "url": "https://devyatkin.dev/55"},
            "type": "product",
        },
        {
            "attributes": {"name": "test56", "url": "https://devyatkin.dev/56"},
            "type": "product",
        },
        {
            "attributes": {"name": "test57", "url": "https://devyatkin.dev/57"},
            "type": "product",
        },
        {
            "attributes": {"name": "test58", "url": "https://devyatkin.dev/58"},
            "type": "product",
        },
        {
            "attributes": {"name": "test59", "url": "https://devyatkin.dev/59"},
            "type": "product",
        },
        {
            "attributes": {"name": "test60", "url": "https://devyatkin.dev/60"},
            "type": "product",
        },
        {
            "attributes": {"name": "test61", "url": "https://devyatkin.dev/61"},
            "type": "product",
        },
        {
            "attributes": {"name": "test62", "url": "https://devyatkin.dev/62"},
            "type": "product",
        },
        {
            "attributes": {"name": "test63", "url": "https://devyatkin.dev/63"},
            "type": "product",
        },
        {
            "attributes": {"name": "test64", "url": "https://devyatkin.dev/64"},
            "type": "product",
        },
        {
            "attributes": {"name": "test65", "url": "https://devyatkin.dev/65"},
            "type": "product",
        },
        {
            "attributes": {"name": "test66", "url": "https://devyatkin.dev/66"},
            "type": "product",
        },
        {
            "attributes": {"name": "test67", "url": "https://devyatkin.dev/67"},
            "type": "product",
        },
        {
            "attributes": {"name": "test68", "url": "https://devyatkin.dev/68"},
            "type": "product",
        },
        {
            "attributes": {"name": "test69", "url": "https://devyatkin.dev/69"},
            "type": "product",
        },
        {
            "attributes": {"name": "test70", "url": "https://devyatkin.dev/70"},
            "type": "product",
        },
        {
            "attributes": {"name": "test71", "url": "https://devyatkin.dev/71"},
            "type": "product",
        },
        {
            "attributes": {"name": "test72", "url": "https://devyatkin.dev/72"},
            "type": "product",
        },
        {
            "attributes": {"name": "test73", "url": "https://devyatkin.dev/73"},
            "type": "product",
        },
        {
            "attributes": {"name": "test74", "url": "https://devyatkin.dev/74"},
            "type": "product",
        },
        {
            "attributes": {"name": "test75", "url": "https://devyatkin.dev/75"},
            "type": "product",
        },
        {
            "attributes": {"name": "test76", "url": "https://devyatkin.dev/76"},
            "type": "product",
        },
        {
            "attributes": {"name": "test77", "url": "https://devyatkin.dev/77"},
            "type": "product",
        },
        {
            "attributes": {"name": "test78", "url": "https://devyatkin.dev/78"},
            "type": "product",
        },
        {
            "attributes": {"name": "test79", "url": "https://devyatkin.dev/79"},
            "type": "product",
        },
        {
            "attributes": {"name": "test80", "url": "https://devyatkin.dev/80"},
            "type": "product",
        },
        {
            "attributes": {"name": "test81", "url": "https://devyatkin.dev/81"},
            "type": "product",
        },
        {
            "attributes": {"name": "test82", "url": "https://devyatkin.dev/82"},
            "type": "product",
        },
        {
            "attributes": {"name": "test83", "url": "https://devyatkin.dev/83"},
            "type": "product",
        },
        {
            "attributes": {"name": "test84", "url": "https://devyatkin.dev/84"},
            "type": "product",
        },
        {
            "attributes": {"name": "test85", "url": "https://devyatkin.dev/85"},
            "type": "product",
        },
        {
            "attributes": {"name": "test86", "url": "https://devyatkin.dev/86"},
            "type": "product",
        },
        {
            "attributes": {"name": "test87", "url": "https://devyatkin.dev/87"},
            "type": "product",
        },
        {
            "attributes": {"name": "test88", "url": "https://devyatkin.dev/88"},
            "type": "product",
        },
        {
            "attributes": {"name": "test89", "url": "https://devyatkin.dev/89"},
            "type": "product",
        },
        {
            "attributes": {"name": "test90", "url": "https://devyatkin.dev/90"},
            "type": "product",
        },
        {
            "attributes": {"name": "test91", "url": "https://devyatkin.dev/91"},
            "type": "product",
        },
        {
            "attributes": {"name": "test92", "url": "https://devyatkin.dev/92"},
            "type": "product",
        },
        {
            "attributes": {"name": "test93", "url": "https://devyatkin.dev/93"},
            "type": "product",
        },
        {
            "attributes": {"name": "test94", "url": "https://devyatkin.dev/94"},
            "type": "product",
        },
        {
            "attributes": {"name": "test95", "url": "https://devyatkin.dev/95"},
            "type": "product",
        },
        {
            "attributes": {"name": "test96", "url": "https://devyatkin.dev/96"},
            "type": "product",
        },
        {
            "attributes": {"name": "test97", "url": "https://devyatkin.dev/97"},
            "type": "product",
        },
        {
            "attributes": {"name": "test98", "url": "https://devyatkin.dev/98"},
            "type": "product",
        },
        {
            "attributes": {"name": "test99", "url": "https://devyatkin.dev/99"},
            "type": "product",
        },
        {
            "attributes": {"name": "test100", "url": "https://devyatkin.dev/100"},
            "type": "product",
        },
    ],
    "page": 2,
    "size": 50,
    "total": 149,
}

snapshots["TestProductPaginator.test_reduced_qs_paginator 1"] = {
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
        {
            "attributes": {"name": "test10", "url": "https://devyatkin.dev/10"},
            "type": "product",
        },
    ],
    "page": 1,
    "size": 10,
    "total": 149,
}

snapshots["TestWPPaginator.test_default_paginator 1"] = {
    "data": [
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
    ],
    "page": 1,
    "size": 50,
    "total": 149,
}

snapshots["TestWPPaginator.test_empty_page_reduced_qs_paginator 1"] = {
    "data": [],
    "page": 16,
    "size": 10,
    "total": 149,
}

snapshots["TestWPPaginator.test_first_page_paginator 1"] = {
    "data": [
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
    ],
    "page": 1,
    "size": 50,
    "total": 149,
}

snapshots["TestWPPaginator.test_last_page_paginator 1"] = {
    "data": [
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
    ],
    "page": 3,
    "size": 50,
    "total": 149,
}

snapshots["TestWPPaginator.test_last_page_reduced_qs_paginator 1"] = {
    "data": [
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
    ],
    "page": 15,
    "size": 10,
    "total": 149,
}

snapshots["TestWPPaginator.test_next_page_paginator 1"] = {
    "data": [
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
    ],
    "page": 2,
    "size": 50,
    "total": 149,
}

snapshots["TestWPPaginator.test_reduced_qs_paginator 1"] = {
    "data": [
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
        {
            "attributes": {"reserved": False, "substitutable": True},
            "type": "wishlist_products",
        },
    ],
    "page": 1,
    "size": 10,
    "total": 149,
}

snapshots["TestWishlistPaginator.test_default_paginator 1"] = {
    "data": [
        {"attributes": {"name": "test1"}, "type": "wishlist"},
        {"attributes": {"name": "test2"}, "type": "wishlist"},
        {"attributes": {"name": "test3"}, "type": "wishlist"},
        {"attributes": {"name": "test4"}, "type": "wishlist"},
        {"attributes": {"name": "test5"}, "type": "wishlist"},
        {"attributes": {"name": "test6"}, "type": "wishlist"},
        {"attributes": {"name": "test7"}, "type": "wishlist"},
        {"attributes": {"name": "test8"}, "type": "wishlist"},
        {"attributes": {"name": "test9"}, "type": "wishlist"},
        {"attributes": {"name": "test10"}, "type": "wishlist"},
        {"attributes": {"name": "test11"}, "type": "wishlist"},
        {"attributes": {"name": "test12"}, "type": "wishlist"},
        {"attributes": {"name": "test13"}, "type": "wishlist"},
        {"attributes": {"name": "test14"}, "type": "wishlist"},
        {"attributes": {"name": "test15"}, "type": "wishlist"},
        {"attributes": {"name": "test16"}, "type": "wishlist"},
        {"attributes": {"name": "test17"}, "type": "wishlist"},
        {"attributes": {"name": "test18"}, "type": "wishlist"},
        {"attributes": {"name": "test19"}, "type": "wishlist"},
        {"attributes": {"name": "test20"}, "type": "wishlist"},
        {"attributes": {"name": "test21"}, "type": "wishlist"},
        {"attributes": {"name": "test22"}, "type": "wishlist"},
        {"attributes": {"name": "test23"}, "type": "wishlist"},
        {"attributes": {"name": "test24"}, "type": "wishlist"},
        {"attributes": {"name": "test25"}, "type": "wishlist"},
        {"attributes": {"name": "test26"}, "type": "wishlist"},
        {"attributes": {"name": "test27"}, "type": "wishlist"},
        {"attributes": {"name": "test28"}, "type": "wishlist"},
        {"attributes": {"name": "test29"}, "type": "wishlist"},
        {"attributes": {"name": "test30"}, "type": "wishlist"},
        {"attributes": {"name": "test31"}, "type": "wishlist"},
        {"attributes": {"name": "test32"}, "type": "wishlist"},
        {"attributes": {"name": "test33"}, "type": "wishlist"},
        {"attributes": {"name": "test34"}, "type": "wishlist"},
        {"attributes": {"name": "test35"}, "type": "wishlist"},
        {"attributes": {"name": "test36"}, "type": "wishlist"},
        {"attributes": {"name": "test37"}, "type": "wishlist"},
        {"attributes": {"name": "test38"}, "type": "wishlist"},
        {"attributes": {"name": "test39"}, "type": "wishlist"},
        {"attributes": {"name": "test40"}, "type": "wishlist"},
        {"attributes": {"name": "test41"}, "type": "wishlist"},
        {"attributes": {"name": "test42"}, "type": "wishlist"},
        {"attributes": {"name": "test43"}, "type": "wishlist"},
        {"attributes": {"name": "test44"}, "type": "wishlist"},
        {"attributes": {"name": "test45"}, "type": "wishlist"},
        {"attributes": {"name": "test46"}, "type": "wishlist"},
        {"attributes": {"name": "test47"}, "type": "wishlist"},
        {"attributes": {"name": "test48"}, "type": "wishlist"},
        {"attributes": {"name": "test49"}, "type": "wishlist"},
        {"attributes": {"name": "test50"}, "type": "wishlist"},
    ],
    "page": 1,
    "size": 50,
    "total": 149,
}

snapshots["TestWishlistPaginator.test_empty_page_reduced_qs_paginator 1"] = {
    "data": [],
    "page": 16,
    "size": 10,
    "total": 149,
}

snapshots["TestWishlistPaginator.test_first_page_paginator 1"] = {
    "data": [
        {"attributes": {"name": "test1"}, "type": "wishlist"},
        {"attributes": {"name": "test2"}, "type": "wishlist"},
        {"attributes": {"name": "test3"}, "type": "wishlist"},
        {"attributes": {"name": "test4"}, "type": "wishlist"},
        {"attributes": {"name": "test5"}, "type": "wishlist"},
        {"attributes": {"name": "test6"}, "type": "wishlist"},
        {"attributes": {"name": "test7"}, "type": "wishlist"},
        {"attributes": {"name": "test8"}, "type": "wishlist"},
        {"attributes": {"name": "test9"}, "type": "wishlist"},
        {"attributes": {"name": "test10"}, "type": "wishlist"},
        {"attributes": {"name": "test11"}, "type": "wishlist"},
        {"attributes": {"name": "test12"}, "type": "wishlist"},
        {"attributes": {"name": "test13"}, "type": "wishlist"},
        {"attributes": {"name": "test14"}, "type": "wishlist"},
        {"attributes": {"name": "test15"}, "type": "wishlist"},
        {"attributes": {"name": "test16"}, "type": "wishlist"},
        {"attributes": {"name": "test17"}, "type": "wishlist"},
        {"attributes": {"name": "test18"}, "type": "wishlist"},
        {"attributes": {"name": "test19"}, "type": "wishlist"},
        {"attributes": {"name": "test20"}, "type": "wishlist"},
        {"attributes": {"name": "test21"}, "type": "wishlist"},
        {"attributes": {"name": "test22"}, "type": "wishlist"},
        {"attributes": {"name": "test23"}, "type": "wishlist"},
        {"attributes": {"name": "test24"}, "type": "wishlist"},
        {"attributes": {"name": "test25"}, "type": "wishlist"},
        {"attributes": {"name": "test26"}, "type": "wishlist"},
        {"attributes": {"name": "test27"}, "type": "wishlist"},
        {"attributes": {"name": "test28"}, "type": "wishlist"},
        {"attributes": {"name": "test29"}, "type": "wishlist"},
        {"attributes": {"name": "test30"}, "type": "wishlist"},
        {"attributes": {"name": "test31"}, "type": "wishlist"},
        {"attributes": {"name": "test32"}, "type": "wishlist"},
        {"attributes": {"name": "test33"}, "type": "wishlist"},
        {"attributes": {"name": "test34"}, "type": "wishlist"},
        {"attributes": {"name": "test35"}, "type": "wishlist"},
        {"attributes": {"name": "test36"}, "type": "wishlist"},
        {"attributes": {"name": "test37"}, "type": "wishlist"},
        {"attributes": {"name": "test38"}, "type": "wishlist"},
        {"attributes": {"name": "test39"}, "type": "wishlist"},
        {"attributes": {"name": "test40"}, "type": "wishlist"},
        {"attributes": {"name": "test41"}, "type": "wishlist"},
        {"attributes": {"name": "test42"}, "type": "wishlist"},
        {"attributes": {"name": "test43"}, "type": "wishlist"},
        {"attributes": {"name": "test44"}, "type": "wishlist"},
        {"attributes": {"name": "test45"}, "type": "wishlist"},
        {"attributes": {"name": "test46"}, "type": "wishlist"},
        {"attributes": {"name": "test47"}, "type": "wishlist"},
        {"attributes": {"name": "test48"}, "type": "wishlist"},
        {"attributes": {"name": "test49"}, "type": "wishlist"},
        {"attributes": {"name": "test50"}, "type": "wishlist"},
    ],
    "page": 1,
    "size": 50,
    "total": 149,
}

snapshots["TestWishlistPaginator.test_last_page_paginator 1"] = {
    "data": [
        {"attributes": {"name": "test101"}, "type": "wishlist"},
        {"attributes": {"name": "test102"}, "type": "wishlist"},
        {"attributes": {"name": "test103"}, "type": "wishlist"},
        {"attributes": {"name": "test104"}, "type": "wishlist"},
        {"attributes": {"name": "test105"}, "type": "wishlist"},
        {"attributes": {"name": "test106"}, "type": "wishlist"},
        {"attributes": {"name": "test107"}, "type": "wishlist"},
        {"attributes": {"name": "test108"}, "type": "wishlist"},
        {"attributes": {"name": "test109"}, "type": "wishlist"},
        {"attributes": {"name": "test110"}, "type": "wishlist"},
        {"attributes": {"name": "test111"}, "type": "wishlist"},
        {"attributes": {"name": "test112"}, "type": "wishlist"},
        {"attributes": {"name": "test113"}, "type": "wishlist"},
        {"attributes": {"name": "test114"}, "type": "wishlist"},
        {"attributes": {"name": "test115"}, "type": "wishlist"},
        {"attributes": {"name": "test116"}, "type": "wishlist"},
        {"attributes": {"name": "test117"}, "type": "wishlist"},
        {"attributes": {"name": "test118"}, "type": "wishlist"},
        {"attributes": {"name": "test119"}, "type": "wishlist"},
        {"attributes": {"name": "test120"}, "type": "wishlist"},
        {"attributes": {"name": "test121"}, "type": "wishlist"},
        {"attributes": {"name": "test122"}, "type": "wishlist"},
        {"attributes": {"name": "test123"}, "type": "wishlist"},
        {"attributes": {"name": "test124"}, "type": "wishlist"},
        {"attributes": {"name": "test125"}, "type": "wishlist"},
        {"attributes": {"name": "test126"}, "type": "wishlist"},
        {"attributes": {"name": "test127"}, "type": "wishlist"},
        {"attributes": {"name": "test128"}, "type": "wishlist"},
        {"attributes": {"name": "test129"}, "type": "wishlist"},
        {"attributes": {"name": "test130"}, "type": "wishlist"},
        {"attributes": {"name": "test131"}, "type": "wishlist"},
        {"attributes": {"name": "test132"}, "type": "wishlist"},
        {"attributes": {"name": "test133"}, "type": "wishlist"},
        {"attributes": {"name": "test134"}, "type": "wishlist"},
        {"attributes": {"name": "test135"}, "type": "wishlist"},
        {"attributes": {"name": "test136"}, "type": "wishlist"},
        {"attributes": {"name": "test137"}, "type": "wishlist"},
        {"attributes": {"name": "test138"}, "type": "wishlist"},
        {"attributes": {"name": "test139"}, "type": "wishlist"},
        {"attributes": {"name": "test140"}, "type": "wishlist"},
        {"attributes": {"name": "test141"}, "type": "wishlist"},
        {"attributes": {"name": "test142"}, "type": "wishlist"},
        {"attributes": {"name": "test143"}, "type": "wishlist"},
        {"attributes": {"name": "test144"}, "type": "wishlist"},
        {"attributes": {"name": "test145"}, "type": "wishlist"},
        {"attributes": {"name": "test146"}, "type": "wishlist"},
        {"attributes": {"name": "test147"}, "type": "wishlist"},
        {"attributes": {"name": "test148"}, "type": "wishlist"},
        {"attributes": {"name": "test149"}, "type": "wishlist"},
    ],
    "page": 3,
    "size": 50,
    "total": 149,
}

snapshots["TestWishlistPaginator.test_last_page_reduced_qs_paginator 1"] = {
    "data": [
        {"attributes": {"name": "test141"}, "type": "wishlist"},
        {"attributes": {"name": "test142"}, "type": "wishlist"},
        {"attributes": {"name": "test143"}, "type": "wishlist"},
        {"attributes": {"name": "test144"}, "type": "wishlist"},
        {"attributes": {"name": "test145"}, "type": "wishlist"},
        {"attributes": {"name": "test146"}, "type": "wishlist"},
        {"attributes": {"name": "test147"}, "type": "wishlist"},
        {"attributes": {"name": "test148"}, "type": "wishlist"},
        {"attributes": {"name": "test149"}, "type": "wishlist"},
    ],
    "page": 15,
    "size": 10,
    "total": 149,
}

snapshots["TestWishlistPaginator.test_next_page_paginator 1"] = {
    "data": [
        {"attributes": {"name": "test51"}, "type": "wishlist"},
        {"attributes": {"name": "test52"}, "type": "wishlist"},
        {"attributes": {"name": "test53"}, "type": "wishlist"},
        {"attributes": {"name": "test54"}, "type": "wishlist"},
        {"attributes": {"name": "test55"}, "type": "wishlist"},
        {"attributes": {"name": "test56"}, "type": "wishlist"},
        {"attributes": {"name": "test57"}, "type": "wishlist"},
        {"attributes": {"name": "test58"}, "type": "wishlist"},
        {"attributes": {"name": "test59"}, "type": "wishlist"},
        {"attributes": {"name": "test60"}, "type": "wishlist"},
        {"attributes": {"name": "test61"}, "type": "wishlist"},
        {"attributes": {"name": "test62"}, "type": "wishlist"},
        {"attributes": {"name": "test63"}, "type": "wishlist"},
        {"attributes": {"name": "test64"}, "type": "wishlist"},
        {"attributes": {"name": "test65"}, "type": "wishlist"},
        {"attributes": {"name": "test66"}, "type": "wishlist"},
        {"attributes": {"name": "test67"}, "type": "wishlist"},
        {"attributes": {"name": "test68"}, "type": "wishlist"},
        {"attributes": {"name": "test69"}, "type": "wishlist"},
        {"attributes": {"name": "test70"}, "type": "wishlist"},
        {"attributes": {"name": "test71"}, "type": "wishlist"},
        {"attributes": {"name": "test72"}, "type": "wishlist"},
        {"attributes": {"name": "test73"}, "type": "wishlist"},
        {"attributes": {"name": "test74"}, "type": "wishlist"},
        {"attributes": {"name": "test75"}, "type": "wishlist"},
        {"attributes": {"name": "test76"}, "type": "wishlist"},
        {"attributes": {"name": "test77"}, "type": "wishlist"},
        {"attributes": {"name": "test78"}, "type": "wishlist"},
        {"attributes": {"name": "test79"}, "type": "wishlist"},
        {"attributes": {"name": "test80"}, "type": "wishlist"},
        {"attributes": {"name": "test81"}, "type": "wishlist"},
        {"attributes": {"name": "test82"}, "type": "wishlist"},
        {"attributes": {"name": "test83"}, "type": "wishlist"},
        {"attributes": {"name": "test84"}, "type": "wishlist"},
        {"attributes": {"name": "test85"}, "type": "wishlist"},
        {"attributes": {"name": "test86"}, "type": "wishlist"},
        {"attributes": {"name": "test87"}, "type": "wishlist"},
        {"attributes": {"name": "test88"}, "type": "wishlist"},
        {"attributes": {"name": "test89"}, "type": "wishlist"},
        {"attributes": {"name": "test90"}, "type": "wishlist"},
        {"attributes": {"name": "test91"}, "type": "wishlist"},
        {"attributes": {"name": "test92"}, "type": "wishlist"},
        {"attributes": {"name": "test93"}, "type": "wishlist"},
        {"attributes": {"name": "test94"}, "type": "wishlist"},
        {"attributes": {"name": "test95"}, "type": "wishlist"},
        {"attributes": {"name": "test96"}, "type": "wishlist"},
        {"attributes": {"name": "test97"}, "type": "wishlist"},
        {"attributes": {"name": "test98"}, "type": "wishlist"},
        {"attributes": {"name": "test99"}, "type": "wishlist"},
        {"attributes": {"name": "test100"}, "type": "wishlist"},
    ],
    "page": 2,
    "size": 50,
    "total": 149,
}

snapshots["TestWishlistPaginator.test_reduced_qs_paginator 1"] = {
    "data": [
        {"attributes": {"name": "test1"}, "type": "wishlist"},
        {"attributes": {"name": "test2"}, "type": "wishlist"},
        {"attributes": {"name": "test3"}, "type": "wishlist"},
        {"attributes": {"name": "test4"}, "type": "wishlist"},
        {"attributes": {"name": "test5"}, "type": "wishlist"},
        {"attributes": {"name": "test6"}, "type": "wishlist"},
        {"attributes": {"name": "test7"}, "type": "wishlist"},
        {"attributes": {"name": "test8"}, "type": "wishlist"},
        {"attributes": {"name": "test9"}, "type": "wishlist"},
        {"attributes": {"name": "test10"}, "type": "wishlist"},
    ],
    "page": 1,
    "size": 10,
    "total": 149,
}
