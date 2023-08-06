from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .importers.import_observations import import_observations

# Schemas
FredObservation = schema_from_yaml_file(
    Path(__file__).parent / "schemas/FredObservation.yml"
)
FredSeries = schema_from_yaml_file(Path(__file__).parent / "schemas/FredSeries.yml")
