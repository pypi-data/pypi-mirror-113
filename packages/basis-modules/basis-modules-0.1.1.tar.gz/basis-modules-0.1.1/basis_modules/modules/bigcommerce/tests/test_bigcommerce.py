from basis_modules.helpers.testing import TestImporter
from basis_modules.modules import bigcommerce

test_orders = TestImporter(
    function_key="bigcommerce.import_orders",
    module=bigcommerce,
    params_from_env={
        "store_id": "TEST_BIGCOMMERCE_STORE_ID",
        "api_key": "TEST_BIGCOMMERCE_API_KEY",
    },
    expected_records_cnt=1,
)

test_order_products = TestImporter(
    function_key="bigcommerce.import_order_products",
    module=bigcommerce,
    params_from_env={
        "store_id": "TEST_BIGCOMMERCE_STORE_ID",
        "api_key": "TEST_BIGCOMMERCE_API_KEY",
    },
    expected_records_cnt=1,
)


def test(interactive=False):
    test_orders.run(interactive=interactive)
    test_order_products.run(interactive=interactive)


if __name__ == "__main__":
    test(interactive=True)
