from typing import TypeVar

from basis.core.module import BasisModule

Transaction = TypeVar("Transaction")

module = BasisModule(
    "bi",
    py_module_path=__file__,
    py_module_name=__name__,
)
