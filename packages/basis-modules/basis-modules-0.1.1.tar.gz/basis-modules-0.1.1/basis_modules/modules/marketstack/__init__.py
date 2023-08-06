from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .importers.import_tickers import import_tickers
from .transformers.conform_tickers import conform_tickers

# Schemas
MarketstackTicker = schema_from_yaml_file(
    Path(__file__).parent / "schemas/MarketstackTicker.yml"
)
