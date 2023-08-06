from basis_modules.helpers.testing import TestImporter
from basis_modules.modules import stripe

TEST_API_KEY = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


test_charges = TestImporter(
    function_key="stripe.import_charges",
    module=stripe,
    params={"api_key": TEST_API_KEY},
    params_from_env={"api_key": "TEST_STRIPE_API_KEY"},
    expected_records_cnt=100,
    expected_records_field="amount",
)


def test():
    test_charges()


if __name__ == "__main__":
    test_charges.run(interactive=True)
