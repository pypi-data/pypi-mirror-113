from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Dict, Iterator, List, Tuple

from basis import Context, datafunction
from basis.core.extraction.connection import JsonHttpApiConnection
from basis_modules.modules.square.importers.import_payments import (
    BASE_URL,
    DEFAULT_MIN_DATE,
)
from dcp.data_format import Records
from requests.auth import HTTPBasicAuth

if TYPE_CHECKING:
    from basis_modules.modules.square import SquareOrder


@datafunction(
    namespace="square",
    display_name="Import Square Orders",
)
def import_orders(
    ctx: Context, access_token: str, api_url: str = BASE_URL
) -> Iterator[Records[SquareOrder]]:
    payments_url = api_url.strip("/") + "/payments"
    orders_url = api_url.strip("/") + "/orders/batch-retrieve"
    location_url = api_url.strip("/") + "/locations"
    conn = JsonHttpApiConnection(
        date_format="%FT%TZ",
        default_headers={"Authorization": f"Bearer {access_token}"},
    )
    for location in conn.get(location_url).json()["locations"]:
        state_key = f"{location['id']}.latest_created_at"
        latest_created_at = ctx.get_state_value(state_key) or DEFAULT_MIN_DATE

        params = {
            "sort_order": "ASC",
            "begin_time": latest_created_at,
            "location_id": location["id"],
        }
        while ctx.should_continue():
            resp = conn.get(
                payments_url,
                params,
            )
            json_resp = resp.json()
            assert isinstance(json_resp, dict)
            payment_records = json_resp["payments"]
            if len(payment_records) == 0:
                # All done
                break

            # Fetch orders for payments
            order_ids = [r["order_id"] for r in payment_records if r.get("order_id")]
            orders_resp = conn.post(orders_url, {"order_ids": order_ids})
            orders_json_resp = orders_resp.json()
            assert isinstance(orders_json_resp, dict)
            order_records = orders_json_resp["orders"]
            yield order_records

            new_latest_created_at = max([o["created_at"] for o in payment_records])
            ctx.emit_state_value(state_key, new_latest_created_at)
            cursor = json_resp.get("cursor")
            if not cursor:
                break
            params["cursor"] = cursor
