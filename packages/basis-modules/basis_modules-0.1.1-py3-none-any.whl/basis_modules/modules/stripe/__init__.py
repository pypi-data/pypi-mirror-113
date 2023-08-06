from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .importers.import_charges import import_charges
from .importers.import_invoices import import_invoices
from .importers.import_refunds import import_refunds
from .importers.import_subscription_items import import_subscription_items
from .importers.import_subscriptions import import_subscriptions
from .transformers.clean_charges import clean_charges

# Schemas
StripeCharge = schema_from_yaml_file(Path(__file__).parent / "schemas/StripeCharge.yml")
StripeChargeRaw = schema_from_yaml_file(
    Path(__file__).parent / "schemas/StripeChargeRaw.yml"
)
StripeRefundRaw = schema_from_yaml_file(
    Path(__file__).parent / "schemas/StripeRefundRaw.yml"
)
StripeSubscriptionRaw = schema_from_yaml_file(
    Path(__file__).parent / "schemas/StripeSubscriptionRaw.yml"
)
StripeSubscriptionItemRaw = schema_from_yaml_file(
    Path(__file__).parent / "schemas/StripeSubscriptionItemRaw.yml"
)
StripeInvoiceRaw = schema_from_yaml_file(
    Path(__file__).parent / "schemas/StripeInvoiceRaw.yml"
)
