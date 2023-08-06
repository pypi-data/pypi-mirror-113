from basis_modules.helpers.testing import TestImporter
from basis_modules.modules import square

test_payments = TestImporter(
    function_key="square.import_payments",
    module=square,
    # params={},
    params_from_env={"access_token": "TEST_SQUARE_ACCESS_TOKEN"},
    expected_records_cnt=100,
    expected_records_field="total_money",
)
test_orders = TestImporter(
    function_key="square.import_orders",
    module=square,
    # params={},
    params_from_env={"access_token": "TEST_SQUARE_ACCESS_TOKEN"},
    expected_records_cnt=1,
    expected_records_field="id",
)


def test(interactive=False):
    test_payments.run(interactive=interactive)
    test_orders.run(interactive=interactive)


if __name__ == "__main__":
    test(interactive=True)
