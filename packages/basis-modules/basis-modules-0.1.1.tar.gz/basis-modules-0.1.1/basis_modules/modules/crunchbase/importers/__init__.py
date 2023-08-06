from __future__ import annotations

import io
import os
import tarfile

from basis import DataFunctionContext
from basis.helpers.connectors.connection import HttpApiConnection
from dcp.data_format import CsvFileFormat
from dcp.utils.common import utcnow

BULK_CSV_URL = "https://api.crunchbase.com/bulk/v4/bulk_export.tar.gz"
BULK_CSV_SAMPLE_URL = (
    "https://static.crunchbase.com/data_crunchbase/bulk_export_sample.tar.gz"
)
CRUNCHBASE_CSV_TO_SCHEMA_MAP = {
    "organizations": "crunchbase.CrunchbaseOrganization",
    "people": "crunchbase.CrunchbasePerson",
    "funding_rounds": "crunchbase.CrunchbaseFundingRound",
}


def base_import(
    data_source: str, ctx: DataFunctionContext, user_key: str, use_sample: bool = False
):
    params = {
        "user_key": user_key,
    }
    url = BULK_CSV_SAMPLE_URL if use_sample else BULK_CSV_URL

    while ctx.should_continue():
        resp = HttpApiConnection().get(
            url=url,
            params=params,
        )

        ib = io.BytesIO(resp.content)

        with tarfile.open(fileobj=ib) as csv_files:
            raw = csv_files.extractfile("{}.csv".format(data_source))
            ctx.emit_state_value("imported_{}".format(data_source), True)
            ctx.emit(
                raw,
                data_format=CsvFileFormat,
                schema=CRUNCHBASE_CSV_TO_SCHEMA_MAP[data_source],
            )
            ctx.emit_state_value("latest_imported_at".format(data_source), utcnow())

        return
