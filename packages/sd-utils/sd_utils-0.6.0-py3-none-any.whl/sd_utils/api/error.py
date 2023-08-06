from abc import ABC
from typing import Any, Callable, Dict, Optional


def default_error_func(status_code: int, content: Dict[str, Any]) -> bool:
    return False


class Error(ABC):
    SLUG = "__api_error_"

    def __init__(
        self,
        code: int,
        message: str,
        error_func: Optional[Callable[[int, Dict[str, Any]], bool]] = None,
    ):
        self._code = code
        self._message = message
        self.error_func = (
            error_func if error_func is not None else default_error_func
        )

    def __set_name__(self, owner: Any, name: str):
        self.private_name = Error.SLUG + name

    def __get__(self, obj: Any, objtype: Any = None):
        return getattr(obj, self.private_name)

    def __set__(self, obj: Any, value: Any):
        setattr(obj, self.private_name, value)

    def set_api_name(self, name: str):
        self.api_name = name

    def is_error(
        self, status_code: int, content: Dict[str, Any]
    ) -> Optional[bool]:
        return self.error_func(status_code, content)

    @property
    def code(self) -> int:
        return self._code

    @property
    def message(self) -> str:
        return self._message
