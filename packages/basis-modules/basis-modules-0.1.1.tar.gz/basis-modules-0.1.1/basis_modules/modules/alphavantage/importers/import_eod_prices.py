from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional

from basis import Context, DataBlock, Reference, datafunction
from basis.core.extraction.connection import JsonHttpApiConnection
from basis_modules.modules.alphavantage.importers.base import (
    ALPHAVANTAGE_API_BASE_URL,
    MIN_DATETIME,
    is_alphavantage_error,
    is_alphavantage_rate_limit,
    prepare_params_for_ticker,
    prepare_tickers,
)
from dcp.data_format.formats.memory.records import Records
from dcp.utils.common import (
    ensure_date,
    ensure_datetime,
    ensure_utc,
    title_to_snake_case,
    utcnow,
)
from dcp.utils.data import read_csv

if TYPE_CHECKING:
    from basis_modules.modules.stocks import Ticker
    from basis_modules.modules.alphavantage import AlphavantageEodPrice


@datafunction(
    "import_eod_prices",
    namespace="alphavantage",
    display_name="Import Alphavantage EOD prices",
)
def import_eod_prices(
    ctx: Context,
    tickers_input: Optional[Reference[Ticker]],
    api_key: str,
    tickers: Optional[List] = None,
) -> Iterator[Records[AlphavantageEodPrice]]:
    assert api_key is not None
    tickers = prepare_tickers(tickers, tickers_input)
    if not tickers:
        return None
    ticker_latest_dates_imported = (
        ctx.get_state_value("ticker_latest_dates_imported") or {}
    )
    conn = JsonHttpApiConnection()

    def fetch_prices(params: Dict, tries: int = 0) -> Optional[Records]:
        if tries > 2:
            return None
        resp = conn.get(ALPHAVANTAGE_API_BASE_URL, params, stream=True)
        try:
            record = resp.json()
            # Json response means error
            if is_alphavantage_error(record):
                # TODO: Log this failure?
                print(f"Error for {params} {record}")
                return None
            if is_alphavantage_rate_limit(record):
                time.sleep(60)
                return fetch_prices(params, tries=tries + 1)
        except:
            pass
        # print(resp.raw.read().decode("utf8"))
        # resp.raw.seek(0)
        records = list(read_csv(resp.iter_lines()))
        return records

    for ticker in tickers:
        assert isinstance(ticker, str)
        latest_date_imported = ensure_datetime(
            ticker_latest_dates_imported.get(ticker, MIN_DATETIME)
        )
        assert latest_date_imported is not None
        if utcnow() - ensure_utc(latest_date_imported) < timedelta(days=1):
            # Only check once a day
            continue
        params = prepare_params_for_ticker(ticker, ticker_latest_dates_imported)
        params["apikey"] = api_key
        records = fetch_prices(params)
        if records:
            # Symbol not included
            for r in records:
                r["symbol"] = ticker
            yield records
        # Update state
        ticker_latest_dates_imported[ticker] = utcnow()
        ctx.emit_state_value(
            "ticker_latest_dates_imported", ticker_latest_dates_imported
        )
        if not ctx.should_continue():
            break
