from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .exporters import export_audience

# Schemas
MailchimpMember = schema_from_yaml_file(
    Path(__file__).parent / "schemas/MailchimpMember.yml"
)
