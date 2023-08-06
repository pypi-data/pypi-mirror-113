from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from basis import DataFunctionContext, datafunction

from . import base_import


@dataclass
class ImportCrunchbaseOrganizationsCSVState:
    latest_imported_at: datetime


@datafunction(
    "import_organizations",
    namespace="crunchbase",
    state_class=ImportCrunchbaseOrganizationsCSVState,
    display_name="Import Crunchbase Organizations",
)
def import_organizations(
    ctx: DataFunctionContext,
    user_key: str,
    use_sample: bool = False,
):
    base_import(
        data_source="organizations",
        user_key=user_key,
        ctx=ctx,
        use_sample=use_sample,
    )
