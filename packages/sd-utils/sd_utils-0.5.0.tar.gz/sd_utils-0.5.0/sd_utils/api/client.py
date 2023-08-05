from sd_utils.api.error import Error
from typing import Any, Callable, ClassVar, Dict, Optional, Set
from requests.auth import AuthBase
from sd_utils.api.request import Request


def __inject_base_methods(cls: ClassVar[Any]):
    @classmethod
    def provide_auth(cls: ClassVar[Any], auth: AuthBase):
        for _, v in cls.__dict__.items():
            if isinstance(v, Request):
                v.auth = auth

    setattr(cls, "provide_auth", provide_auth)

    @classmethod
    def requests(cls: ClassVar[Any]) -> Dict[str, Any]:
        response: Dict[str, Any] = {}
        for k, v in cls.__dict__.items():
            if isinstance(v, Request):
                response[k] = v
        return response

    setattr(cls, "requests", requests)

    @classmethod
    def errors(cls: ClassVar[Any]) -> Dict[str, Any]:
        response: Dict[str, Any] = {}
        for k, v in cls.__dict__.items():
            if isinstance(v, Error):
                response[k] = v
        return response

    setattr(cls, "errors", errors)


def client_api(
    base_url: str,
    headers: Dict[str, Any] = {},
    auth: Optional[AuthBase] = None,
) -> Callable[[Any], Any]:
    def decorator(cls: ClassVar[Any]):
        errors: Set[Any] = set()
        for k, v in cls.__dict__.items():
            if isinstance(v, Error):
                errors.add(v)
                v.set_api_name(k)
                setattr(cls, k, v)

        for k, v in cls.__dict__.items():
            if isinstance(v, Request):
                v.configure(base_url, headers, auth, errors)
                setattr(cls, k, v)

        __inject_base_methods(cls)

        return cls

    return decorator
