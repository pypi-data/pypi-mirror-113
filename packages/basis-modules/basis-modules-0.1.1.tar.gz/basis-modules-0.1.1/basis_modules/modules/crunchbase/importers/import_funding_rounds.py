from __future__ import annotations

from basis import DataFunctionContext, datafunction

from . import base_import


@datafunction(
    "import_funding_rounds",
    namespace="crunchbase",
    display_name="Import Crunchbase Funding Rounds",
)
def import_funding_rounds(
    ctx: DataFunctionContext,
    user_key: str,
    use_sample: bool = False,
):
    base_import(
        data_source="funding_rounds",
        user_key=user_key,
        ctx=ctx,
        use_sample=use_sample,
    )
