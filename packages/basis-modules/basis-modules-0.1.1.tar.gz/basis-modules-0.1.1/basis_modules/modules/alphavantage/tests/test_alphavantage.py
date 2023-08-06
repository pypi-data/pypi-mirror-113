from basis_modules.helpers.testing import TestImporter
from basis_modules.modules import alphavantage

test_overview = TestImporter(
    function_key="alphavantage.import_company_overview",
    module=alphavantage,
    params={"tickers": ["AAPL"]},
    params_from_env={"api_key": "TEST_ALPHAVANTAGE_API_KEY"},
    expected_records_cnt=1,
)
test_eod_prices = TestImporter(
    function_key="alphavantage.import_eod_prices",
    module=alphavantage,
    params={"tickers": ["AAPL"]},
    params_from_env={"api_key": "TEST_ALPHAVANTAGE_API_KEY"},
    expected_records_cnt=1,
)


def test(interactive=False):
    test_overview.run(interactive)
    test_eod_prices.run(interactive)


if __name__ == "__main__":
    test(interactive=True)
