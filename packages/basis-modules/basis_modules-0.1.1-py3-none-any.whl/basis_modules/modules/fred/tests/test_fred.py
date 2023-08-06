from basis_modules.helpers.testing import TestImporter
from basis_modules.modules import fred

test_orders = TestImporter(
    function_key="fred.import_observations",
    module=fred,
    params={"series_id": "gdp"},
    params_from_env={"api_key": "TEST_FRED_API_KEY"},
    expected_records_cnt=100,
)


def test(interactive=False):
    test_orders.run(interactive=interactive)


if __name__ == "__main__":
    test(interactive=True)
