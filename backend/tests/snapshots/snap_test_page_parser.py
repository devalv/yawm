# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["TestApi.test_bad_input 1"] = {
    "detail": [
        {
            "loc": ["body", "url"],
            "msg": "invalid or missing URL scheme",
            "type": "value_error.url.scheme",
        }
    ]
}

snapshots["TestApi.test_bad_url 1"] = {"h1": None}

snapshots["TestApi.test_existing_product 1"] = {"h1": "test"}

snapshots["TestApi.test_good_input 1"] = {"h1": "adidas Gazelle"}
