from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .importers.import_company_overview import import_company_overview
from .importers.import_eod_prices import import_eod_prices

# Schemas
AlphavantageEodPrice = schema_from_yaml_file(
    Path(__file__).parent / "schemas/AlphavantageEodPrice.yml"
)
AlphavantageCompanyOverview = schema_from_yaml_file(
    Path(__file__).parent / "schemas/AlphavantageCompanyOverview.yml"
)
