from __future__ import annotations

from typing import TYPE_CHECKING

from basis import Context, DataBlock, datafunction
from pandas.core.frame import DataFrame

if TYPE_CHECKING:
    from basis_modules.modules.stocks import Ticker, EodPrice
    from basis_modules.modules.marketstack import MarketstackTicker


@datafunction(
    namespace="marketstack",
)
def conform_tickers(
    tickers: DataBlock[MarketstackTicker],
) -> DataFrame[Ticker]:
    df = tickers.as_dataframe()
    df["exchange"] = df["exchange_acronym"]
    return df[["symbol", "name", "exchange"]]
