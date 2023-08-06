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
    from basis_modules.modules.alphavantage import AlphavantageCompanyOverview


@datafunction(
    "import_company_overview",
    namespace="alphavantage",
    display_name="Import Alphavantage company overview",
)
def import_company_overview(
    ctx: Context,
    tickers_input: Optional[Reference[Ticker]],
    api_key: str,
    tickers: Optional[List] = None,
) -> Iterator[Records[AlphavantageCompanyOverview]]:
    assert api_key is not None
    tickers = prepare_tickers(tickers, tickers_input)
    if tickers is None:
        # We didn't get an input block for tickers AND
        # the config is empty, so we are done
        return None
    ticker_latest_dates_imported = (
        ctx.get_state_value("ticker_latest_dates_imported") or {}
    )
    conn = JsonHttpApiConnection()
    batch_size = 50
    records = []
    tickers_updated = []

    def fetch_overview(params: Dict, tries: int = 0) -> Optional[Dict]:
        if tries > 2:
            return None
        resp = conn.get(ALPHAVANTAGE_API_BASE_URL, params)
        record = resp.json()
        # Alphavantage returns 200 and json error message on failure
        if is_alphavantage_error(record):
            # TODO: Log this failure?
            # print(f"Error for ticker {params['symbol']}: {record}")
            return None
        if is_alphavantage_rate_limit(record):
            time.sleep(20)
            return fetch_overview(params, tries=tries + 1)
        return record

    for i, ticker in enumerate(tickers):
        assert isinstance(ticker, str)
        latest_date_imported = ensure_datetime(
            ticker_latest_dates_imported.get(ticker, MIN_DATETIME)
        )
        assert latest_date_imported is not None
        # Refresh at most once a day
        # TODO: make this configurable instead of hard-coded 1 day
        if utcnow() - ensure_utc(latest_date_imported) < timedelta(days=1):
            continue
        params = {
            "apikey": api_key,
            "symbol": ticker,
            "function": "OVERVIEW",
        }
        record = fetch_overview(params)
        if not record:
            continue

        # Clean up json keys to be more DB friendly
        record = {title_to_snake_case(k): v for k, v in record.items()}
        records.append(record)
        tickers_updated.append(ticker)
        if len(records) >= batch_size or i == len(tickers) - 1:
            yield records
            # Update state
            for updated_ticker in tickers_updated:
                ticker_latest_dates_imported[updated_ticker] = utcnow()
                ctx.emit_state_value(
                    "ticker_latest_dates_imported", ticker_latest_dates_imported
                )
            if not ctx.should_continue():
                break
            records = []
            tickers_updated = []
