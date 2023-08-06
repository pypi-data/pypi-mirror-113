from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, TYPE_CHECKING, Dict, Iterator, Tuple

from basis import Context, datafunction
from basis.core.extraction.connection import JsonHttpApiConnection
from basis_modules.modules.square.importers.import_payments import (
    BASE_URL,
    DEFAULT_MIN_DATE,
)
from dcp.data_format import Records
from requests.auth import HTTPBasicAuth

if TYPE_CHECKING:
    from basis_modules.modules.square import SquareCatalogObject


@datafunction(
    namespace="square",
    display_name="Import Square Catalog Objects",
)
def import_catalog_objects(
    ctx: Context, access_token: str, api_url: str = BASE_URL
) -> Iterator[Records[SquareCatalogObject]]:
    list_url = api_url.strip("/") + "/catalog/list"
    cursor = ctx.get_state_value("cursor")

    params = {}
    if cursor:
        params["cursor"] = cursor
    conn = JsonHttpApiConnection(
        date_format="%FT%TZ",
        default_headers={"Authorization": f"Bearer {access_token}"},
    )
    while ctx.should_continue():
        resp = conn.get(
            list_url,
            params,
        )
        json_resp = resp.json()
        assert isinstance(json_resp, dict)
        records = json_resp["objects"]
        if len(records) == 0:
            # All done
            break
        yield records
        cursor = json_resp.get("cursor")
        if not cursor:
            break
        params["cursor"] = cursor
        cursor = ctx.emit_state_value("cursor", cursor)
    # TODO: cursor timeout...
    # All done so clear cursor
    cursor = ctx.emit_state_value("cursor", None)
