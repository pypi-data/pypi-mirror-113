from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Dict, Iterator, Tuple

from basis import Context, datafunction
from basis.core.extraction.connection import JsonHttpApiConnection
from basis_modules.modules.square.importers.import_payments import (
    BASE_URL,
    DEFAULT_MIN_DATE,
)
from dcp.data_format import Records
from requests.auth import HTTPBasicAuth

if TYPE_CHECKING:
    from basis_modules.modules.square import SquareCustomer


@datafunction(
    namespace="square",
    display_name="Import Square Customers",
)
def import_customers(
    ctx: Context, access_token: str, api_url: str = BASE_URL
) -> Iterator[Records[SquareCustomer]]:
    endpoint_url = api_url.strip("/") + "/customers"
    latest_created_at = ctx.get_state_value("latest_created_at") or DEFAULT_MIN_DATE

    params = {
        "sort_order": "ASC",
        "sort_field": "CREATED_AT",
        "begin_time": latest_created_at,
    }
    conn = JsonHttpApiConnection(
        date_format="%FT%TZ",
        default_headers={"Authorization": f"Bearer {access_token}"},
    )
    while ctx.should_continue():
        resp = conn.get(
            endpoint_url,
            params,
        )
        json_resp = resp.json()
        assert isinstance(json_resp, dict)
        records = json_resp["customers"]
        if len(records) == 0:
            # All done
            break
        yield records
        new_latest_created_at = max([o["created_at"] for o in records])
        ctx.emit_state({"latest_created_at": new_latest_created_at})
        cursor = json_resp.get("cursor")
        if not cursor:
            break
        params["cursor"] = cursor
