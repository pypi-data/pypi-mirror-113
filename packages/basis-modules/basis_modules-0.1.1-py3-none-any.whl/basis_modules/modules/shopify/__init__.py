from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .importers.import_orders import import_orders

# Schemas
ShopifyOrder = schema_from_yaml_file(Path(__file__).parent / "schemas/ShopifyOrder.yml")
