from sd_utils.api.error import Error
from typing import Any, ClassVar, Dict, Optional, Set
from requests.auth import AuthBase
from sd_utils.api.request import Request


def Client(  # noqa C901
    url: str, headers: Dict[str, Any] = {}, auth: Optional[AuthBase] = None
):
    class client_instance_base(type):
        base_url: str = url

        def __new__(cls, name: str, bases: Any, dct: Any):
            x = super().__new__(cls, name, bases, dct)
            errors: Set[Any] = set()
            for k, v in x.__dict__.items():
                if isinstance(v, Error):
                    errors.add(v)
                    v.set_api_name(k)
                    setattr(cls, k, v)

            for k, v in x.__dict__.items():
                if isinstance(v, Request):
                    v.configure(url, headers, auth, errors)
                    setattr(cls, k, v)

            return x

        @classmethod
        def requests(cls: ClassVar[Any]) -> Dict[str, Any]:
            response: Dict[str, Any] = {}
            for k, v in cls.__dict__.items():
                if isinstance(v, Request):
                    response[k] = v
            return response

        @classmethod
        def errors(cls: ClassVar[Any]) -> Dict[str, Any]:
            response: Dict[str, Any] = {}
            for k, v in cls.__dict__.items():
                if isinstance(v, Error):
                    response[k] = v
            return response

    return client_instance_base
