from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional

import pytz
from basis import Context, DataBlock, Reference, datafunction
from basis.core.extraction.connection import JsonHttpApiConnection
from basis_modules.modules.marketstack.importers.base import (
    HTTPS_MARKETSTACK_API_BASE_URL,
    MARKETSTACK_API_BASE_URL,
    MIN_DATE,
)
from dcp.data_format.formats.memory.records import Records
from dcp.utils.common import ensure_date

if TYPE_CHECKING:
    from basis_modules.modules.stocks import Ticker, EodPrice


@datafunction(
    namespace="marketstack",
    display_name="Import Marketstack EOD prices",
)
def import_eod_prices(
    ctx: Context,
    tickers_input: Optional[Reference[Ticker]],
    access_key: str,
    from_date: date = MIN_DATE,
    tickers: Optional[List] = None,
) -> Iterator[Records[EodPrice]]:
    # access_key = ctx.get_param("access_key")
    use_https = False  # TODO: when do we want this True?
    default_from_date = from_date
    assert access_key is not None
    if tickers_input is not None:
        tickers = list(tickers_input.as_dataframe()["symbol"])
    if not tickers:
        return
    ticker_latest_dates_imported = (
        ctx.get_state_value("ticker_latest_dates_imported") or {}
    )
    conn = JsonHttpApiConnection(date_format="%Y-%m-%d")
    if use_https:
        endpoint_url = HTTPS_MARKETSTACK_API_BASE_URL + "eod"
    else:
        endpoint_url = MARKETSTACK_API_BASE_URL + "eod"
    for ticker in tickers:
        assert isinstance(ticker, str)
        latest_date_imported = ensure_date(
            ticker_latest_dates_imported.get(ticker, default_from_date)
        )
        max_date = latest_date_imported
        params = {
            "limit": 1000,
            "offset": 0,
            "access_key": access_key,
            "symbols": ticker,
            "date_from": latest_date_imported,
        }
        while ctx.should_continue():
            resp = conn.get(endpoint_url, params)
            json_resp = resp.json()
            assert isinstance(json_resp, dict)
            records = json_resp["data"]
            if len(records) == 0:
                # All done
                break
            yield records
            # Update state
            max_date = max(max_date, max(ensure_date(r["date"]) for r in records))
            ticker_latest_dates_imported[ticker] = max_date + timedelta(days=1)
            ctx.emit_state_value(
                "ticker_latest_dates_imported", ticker_latest_dates_imported
            )
            # Setup for next page
            params["offset"] = params["offset"] + len(records)
