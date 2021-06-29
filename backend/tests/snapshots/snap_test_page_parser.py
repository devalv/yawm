# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["TestApi.test_bad_input 1"] = {
    "detail": [
        {
            "loc": ["body", "data", "attributes", "url"],
            "msg": "invalid or missing URL scheme",
            "type": "value_error.url.scheme",
        }
    ]
}

snapshots["TestApi.test_bad_url 1"] = {
    "data": {"attributes": {"h1": None}, "type": "utils"}
}

snapshots["TestApi.test_existing_product 1"] = {
    "data": {"attributes": {"h1": "test"}, "type": "utils"}
}

snapshots["TestApi.test_good_input 1"] = {
    "data": {"attributes": {"h1": "adidas Gazelle"}, "type": "utils"}
}
