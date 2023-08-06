import datetime
from typing import List


class RateLimit:
    def __init__(self, max_requests: int, time_frame: datetime.timedelta):
        self.max_requests = max_requests
        self.time_frame = time_frame
        initial_history: List[datetime.datetime] = []
        self.request_history = initial_history

    def can_make_request(self) -> bool:
        """
        Returns true if the rate limit will not be exceeded
        by making another request
        """
        return (
            len(self.request_history) < self.max_requests
            or self.request_history[0] + self.time_frame
            < datetime.datetime.now()
        )

    def make_request(self) -> None:
        """
        increments the can make request counter
        """
        while (
            len(self.request_history) > 0
            and self.request_history[0] + self.time_frame
            < datetime.datetime.now()
        ):
            self.request_history.pop(0)

        self.request_history.append(datetime.datetime.now())

    def request_wait_time(self) -> int:
        """
        Returns the time in microseconds to wait before the next request
        """
        while (
            len(self.request_history) > 0
            and self.request_history[0] + self.time_frame
            < datetime.datetime.now()
        ):
            self.request_history.pop(0)

        if len(self.request_history) < self.max_requests:
            return 0

        return (
            self.request_history[0].microsecond + self.time_frame.microseconds
        ) - datetime.datetime.now().microsecond
