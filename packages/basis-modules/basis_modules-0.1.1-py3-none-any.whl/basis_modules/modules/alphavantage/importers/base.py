from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional

from basis import Context, DataBlock, Reference, datafunction
from basis.core.extraction.connection import JsonHttpApiConnection
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
    from basis_stocks import (
        Ticker,
        AlphavantageEodPrice,
        AlphavantageCompanyOverview,
    )


ALPHAVANTAGE_API_BASE_URL = "https://www.alphavantage.co/query"
MIN_DATE = date(2000, 1, 1)
MIN_DATETIME = datetime(2000, 1, 1)


def prepare_tickers(
    tickers_list: Optional[List] = None,
    tickers_input: Optional[DataBlock[Ticker]] = None,
) -> Optional[List[str]]:
    tickers = []
    if tickers_input is not None:
        df = tickers_input.as_dataframe()
        tickers = list(df["symbol"])
    else:
        tickers = tickers_list or []
    return tickers


def prepare_params_for_ticker(
    ticker: str, ticker_latest_dates_imported: Dict[str, datetime]
) -> Dict:
    latest_date_imported = ensure_datetime(
        ticker_latest_dates_imported.get(ticker, MIN_DATETIME)
    )
    if ensure_utc(latest_date_imported) <= utcnow() - timedelta(days=100):
        # More than 100 days worth, get full
        outputsize = "full"
    else:
        # Less than 100 days, compact will suffice
        outputsize = "compact"
    params = {
        "symbol": ticker,
        "outputsize": outputsize,
        "datatype": "csv",
        "function": "TIME_SERIES_DAILY_ADJUSTED",
    }
    return params


def is_alphavantage_error(record: Dict) -> bool:
    str_record = str(record).lower()
    return "error message" in str_record or "invalid api call" in str_record


def is_alphavantage_rate_limit(record: Dict) -> bool:
    return (
        "calls per minute" in str(record).lower()
        or "api call volume" in str(record).lower()
    )
