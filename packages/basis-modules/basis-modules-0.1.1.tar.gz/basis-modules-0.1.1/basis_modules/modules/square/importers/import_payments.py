from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, TYPE_CHECKING, Dict, Iterator, Tuple

from basis import Context, datafunction
from basis.core.extraction.connection import JsonHttpApiConnection
from dcp.data_format import Records
from requests.auth import HTTPBasicAuth

if TYPE_CHECKING:
    from basis_modules.modules.square import SquarePayment


BASE_URL = "https://connect.squareup.com/v2/"
DEFAULT_MIN_DATE = datetime(2010, 1, 1)


@datafunction(
    namespace="square",
    display_name="Import Square Payments",
)
def import_payments(
    ctx: Context, access_token: str, api_url: str = BASE_URL
) -> Iterator[Records[SquarePayment]]:
    endpoint_url = api_url.strip("/") + "/payments"
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
            resp = conn.get(endpoint_url, params)
            json_resp = resp.json()
            assert isinstance(json_resp, dict)
            records = json_resp["payments"]
            if len(records) == 0:
                # All done
                break
            # Add location name for convenience
            for r in records:
                r["location_name"] = location["name"]
            yield records
            new_latest_created_at = max([o["created_at"] for o in records])
            ctx.emit_state_value(state_key, new_latest_created_at)
            cursor = json_resp.get("cursor")
            if not cursor:
                break
            params["cursor"] = cursor
