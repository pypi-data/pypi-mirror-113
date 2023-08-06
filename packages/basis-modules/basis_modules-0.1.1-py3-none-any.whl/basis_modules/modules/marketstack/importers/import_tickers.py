from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional

import pytz
from basis import Context, DataBlock, Reference, datafunction
from basis.core.extraction.connection import JsonHttpApiConnection
from basis_modules.modules.marketstack.importers.base import (
    HTTPS_MARKETSTACK_API_BASE_URL,
    MARKETSTACK_API_BASE_URL,
)
from dcp.data_format.formats.memory.records import Records
from dcp.utils.common import ensure_date, ensure_datetime, ensure_utc, utcnow

if TYPE_CHECKING:
    from basis_modules.modules.marketstack import MarketstackTicker


@datafunction(
    namespace="marketstack",
    display_name="Import Marketstack tickers",
)
def import_tickers(
    ctx: Context,
    access_key: str,
    exchanges: List = ["XNYS", "XNAS"],
) -> Iterator[Records[MarketstackTicker]]:
    use_https = False  # TODO: when do we want this True?
    # default_from_date = ctx.get_param("from_date", MIN_DATE)
    assert access_key is not None
    assert isinstance(exchanges, list)
    last_imported_at = ensure_datetime(
        ctx.get_state_value("last_imported_at") or "2020-01-01 00:00:00"
    )
    assert last_imported_at is not None
    last_imported_at = ensure_utc(last_imported_at)
    if utcnow() - last_imported_at < timedelta(days=1):  # TODO: from config
        return
    conn = JsonHttpApiConnection()
    if use_https:
        endpoint_url = HTTPS_MARKETSTACK_API_BASE_URL + "tickers"
    else:
        endpoint_url = MARKETSTACK_API_BASE_URL + "tickers"
    for exchange in exchanges:
        params = {
            "limit": 1000,
            "offset": 0,
            "access_key": access_key,
            "exchange": exchange,
        }
        while ctx.should_continue():
            resp = conn.get(endpoint_url, params)
            json_resp = resp.json()
            assert isinstance(json_resp, dict)
            records = json_resp["data"]
            if len(records) == 0:
                # All done
                break
            # Add a flattened exchange indicator
            for r in records:
                r["exchange_acronym"] = r.get("stock_exchange", {}).get("acronym")
            yield records
            # Setup for next page
            params["offset"] = params["offset"] + len(records)
    ctx.emit_state_value("last_imported_at", utcnow())
