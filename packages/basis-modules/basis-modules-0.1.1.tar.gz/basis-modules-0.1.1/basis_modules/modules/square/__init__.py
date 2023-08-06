from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .importers.import_orders import import_orders
from .importers.import_payments import import_payments
from .importers.import_customers import import_customers
from .importers.import_catalog_objects import import_catalog_objects

# Schemas
SquarePayment = schema_from_yaml_file(
    Path(__file__).parent / "schemas/SquarePayment.yml"
)
SquareOrder = schema_from_yaml_file(Path(__file__).parent / "schemas/SquareOrder.yml")
SquareCustomer = schema_from_yaml_file(
    Path(__file__).parent / "schemas/SquareCustomer.yml"
)
SquareCatalogObject = schema_from_yaml_file(
    Path(__file__).parent / "schemas/SquareCatalogObject.yml"
)
