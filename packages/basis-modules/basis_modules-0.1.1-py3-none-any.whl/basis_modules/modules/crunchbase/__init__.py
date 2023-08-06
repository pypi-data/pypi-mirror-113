from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .importers.import_funding_rounds import import_funding_rounds
from .importers.import_organizations import import_organizations
from .importers.import_people import import_people

# Schemas
CrunchbaseOrganization = schema_from_yaml_file(
    Path(__file__).parent / "schemas/CrunchbaseOrganization.yml"
)
CrunchbaseFundingRound = schema_from_yaml_file(
    Path(__file__).parent / "schemas/CrunchbaseFundingRound.yml"
)
CrunchbasePerson = schema_from_yaml_file(
    Path(__file__).parent / "schemas/CrunchbasePerson.yml"
)
