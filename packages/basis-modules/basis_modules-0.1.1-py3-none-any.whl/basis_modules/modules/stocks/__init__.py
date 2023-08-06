from pathlib import Path

from commonmodel.base import schema_from_yaml_file

# Schemas # No-op
EodPrice = schema_from_yaml_file(Path(__file__).parent / "schemas/EodPrice.yml")
Ticker = schema_from_yaml_file(Path(__file__).parent / "schemas/Ticker.yml")
