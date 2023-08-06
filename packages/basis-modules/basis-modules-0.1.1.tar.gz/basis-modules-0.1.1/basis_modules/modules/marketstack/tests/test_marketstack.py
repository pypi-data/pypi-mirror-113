from basis_modules.helpers.testing import TestImporter
from basis_modules.modules import marketstack

test_tickers = TestImporter(
    function_key="marketstack.import_tickers",
    module=marketstack,
    params={"exchanges": ["XNAS"]},
    params_from_env={"access_key": "TEST_MARKETSTACK_ACCESS_KEY"},
    expected_records_cnt=100,
)

test_eod = TestImporter(
    function_key="marketstack.import_eod_prices",
    module=marketstack,
    params={"tickers": ["AAPL"]},
    params_from_env={"access_key": "TEST_MARKETSTACK_ACCESS_KEY"},
    expected_records_cnt=100,
)


def test(interactive=False):
    test_tickers.run(interactive)
    test_eod.run(interactive)


if __name__ == "__main__":
    test(interactive=True)


# def test_tickers_into_eod():
#     from basis_stocks import module as stocks

#     api_key = ensure_api_key()

#     g = graph()

#     # Initial graph
#     tickers = g.create_node(
#         stocks.functions.marketstack_import_tickers,
#         params={"access_key": api_key, "exchanges": ["XNAS"]},
#     )
#     prices = g.create_node(
#         stocks.functions.marketstack_import_eod_prices,
#         params={"access_key": api_key},
#         inputs={"tickers_input": tickers},
#     )
#     blocks = produce(prices, execution_timelimit_seconds=1, modules=[stocks])
#     records = blocks[0].as_records()
#     assert len(records) >= 100
