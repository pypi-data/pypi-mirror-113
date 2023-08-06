from pathlib import Path

from commonmodel.base import schema_from_yaml_file

# Schemas
PlotlyJson = schema_from_yaml_file(Path(__file__).parent / "schemas/PlotlyJson.yml")
