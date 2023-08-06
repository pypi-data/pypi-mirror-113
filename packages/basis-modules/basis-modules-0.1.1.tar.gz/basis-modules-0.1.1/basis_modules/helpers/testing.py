import os
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Dict, Optional

from basis import DataspaceCfg, Environment, GraphCfg
from dcp.storage.database.utils import get_tmp_sqlite_db_url
from dcp.storage.file_system import get_tmp_local_file_url


def ensure_var(
    varname: str, interactive: bool = True, default: Any = None
) -> Optional[str]:
    var = os.environ.get(varname)
    if var is not None:
        return var
    if interactive:
        var = input(f"Enter {varname} [{default}]: ")
    if var is None:
        var = default
    return var


@dataclass
class TestImporter:
    function_key: str
    module: ModuleType = None
    params: Dict = None
    params_from_env: Dict = None
    expected_records_cnt: int = None
    expected_records_field: str = None

    def get_params(self, interactive: bool):
        params = (self.params or {}).copy()
        for name, envvar in (self.params_from_env or {}).items():
            var = ensure_var(envvar, interactive)
            if var is not None:
                params[name] = var
        return params

    def run(self, interactive: bool = False):
        storage = get_tmp_sqlite_db_url()
        file_storage = get_tmp_local_file_url()
        env = Environment(
            DataspaceCfg(metadata_storage="sqlite://", storages=[storage, file_storage])
        )
        if self.module is not None:
            env.add_module(self.module)

        # Initial graph
        n = GraphCfg(
            key=self.function_key,
            function=self.function_key,
            params=self.get_params(interactive),
        )
        g = GraphCfg(nodes=[n])
        results = env.produce(n.key, g, execution_timelimit_seconds=1)
        records = results[0].stdout().as_records()
        if self.expected_records_cnt is not None:
            assert len(records) >= self.expected_records_cnt
        if self.expected_records_field is not None:
            assert self.expected_records_field in records[0]

    def __call__(self):
        self.run(interactive=False)
