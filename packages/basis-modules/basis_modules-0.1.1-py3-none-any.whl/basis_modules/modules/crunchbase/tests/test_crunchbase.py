from basis_modules.helpers.testing import TestImporter
from basis_modules.modules import crunchbase, shopify

test_orders = TestImporter(
    function_key="crunchbase.import_people",
    module=crunchbase,
    params={"use_sample": True},
    params_from_env={"user_key": "TEST_CRUNCHBASE_USER_KEY"},
    expected_records_cnt=50,
)


def test(interactive=False):
    test_orders.run(interactive=interactive)


if __name__ == "__main__":
    test(interactive=True)
