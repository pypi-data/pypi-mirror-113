from sd_utils.api.rate_limit import RateLimit
from requests.models import Response
from sd_utils.api.error import Error
from typing import Any, Dict, List, Optional, Set, Union
import requests
from requests.auth import AuthBase
import time
from sd_utils.logger import create_logger

logger = create_logger(__file__)


class Request:
    def __init__(
        self,
        method: str,
        endpoint: str,
        body: Dict[str, Any] = {},
        auth: Union[AuthBase, None] = None,
        documentation: str = "",
        rate_limits: List[RateLimit] = [],
    ):
        self.method = method
        self.endpoint = endpoint
        self.body = body
        self.auth = auth
        self._documentation = documentation
        self.rate_limits = rate_limits

    @property
    def documentation(self) -> str:
        return self._documentation

    def __call__(self, query: str = "", body: Dict[str, Any] = {}) -> Any:
        return self._make_request(self.method, query, body)

    def _make_request(  # noqa: C901
        self,
        method: str,
        query: str = "",
        body: Dict[str, Any] = {},
        headers: Dict[str, Any] = {},
        auth: Optional[AuthBase] = None,
    ) -> Any:
        if not self.endpoint.startswith("/"):
            self.endpoint = "/" + self.endpoint
        url = f"{self.base_url}{self.endpoint}"
        if query != "":
            if not query.startswith("/"):
                query = "/" + query
            url += f"{query}"

        data = self.body
        if body != {}:
            data = {**data, **body}

        header_data: Dict[str, Any] = self.headers
        if headers != {}:
            header_data = {**header_data, **headers}

        auth_data = self.auth
        if auth is not None:
            auth_data = auth

        for rate_limit in self.rate_limits:
            while not rate_limit.can_make_request():
                wait_time = rate_limit.request_wait_time() / 1000000.0
                time.sleep(wait_time)  # sleep in us

        response: Response = requests.request(
            method, url, data=data, headers=header_data, auth=auth_data
        )

        for rate_limit in self.rate_limits:
            rate_limit.make_request()

        if response.status_code != 200:  # basic definition of errors
            self.__handle_error(response)
        return response.json()

    def configure(
        self,
        base_url: str,
        headers: Dict[str, Any],
        auth: Optional[AuthBase],
        errors: Set[Error],
    ):
        self.base_url = base_url
        self.headers = headers
        if self.auth is None:
            self.auth = auth
        self.errors = errors

    def __handle_error(self, response: Response):
        for error in self.errors:
            if error.is_error(response.status_code, response.json()):
                # this line raises an exception
                Request.__build_exception(error)

        # no defined error, use default one
        if response.status_code == 404:  # specific default error
            e = Error(
                404,
                f"Not Found. This is a default error thrown by sd_utils. The http url requested does not exist.",
            )
            e.set_api_name("not_found")
        else:
            e = Error(
                400,
                f"Bad Request. This is a default error thrown by sd_utils. This means that the error response was not defined or the request sent was invalid. Error code: {response.status_code}",
            )
            e.set_api_name("bad_request")
        Request.__build_exception(e)

    @staticmethod
    def __build_exception(error: Error):
        def constructor(self: Any):
            super(Exception, self).__init__(f"[{error.code}] {error.message}")

        raise type(
            f"{error.api_name.replace('_', ' ').title().replace(' ', '')}",
            (Exception,),
            {"__init__": constructor},
        )
