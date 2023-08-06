from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .importers.import_order_products import import_order_products
from .importers.import_orders import import_orders

# Schemas
BigCommerceOrder = schema_from_yaml_file(
    Path(__file__).parent / "schemas/BigCommerceOrder.yml"
)
BigCommerceOrderProduct = schema_from_yaml_file(
    Path(__file__).parent / "schemas/BigCommerceOrderProduct.yml"
)
