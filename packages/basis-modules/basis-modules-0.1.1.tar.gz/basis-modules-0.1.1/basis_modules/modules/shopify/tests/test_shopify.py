from basis_modules.helpers.testing import TestImporter
from basis_modules.modules import shopify

test_orders = TestImporter(
    function_key="shopify.import_orders",
    module=shopify,
    params_from_env={"admin_url": "TEST_SHOPIFY_ADMIN_URL"},
    expected_records_cnt=1,
    expected_records_field="id",
)


def test(interactive=False):
    test_orders.run(interactive=interactive)


if __name__ == "__main__":
    test(interactive=True)
