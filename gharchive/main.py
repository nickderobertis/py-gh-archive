import datetime
from typing import Optional

import requests
import gzip
import json

from gharchive.logger import logger
from gharchive.models import Archive

BASE_URL = "https://data.gharchive.org/"


class GHArchive:
    def __init__(self):
        pass

    def get(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        dt: Optional[datetime.datetime] = None,
    ) -> Archive:
        self._validate_get(year, month, day, hour, dt)
        if dt is None:
            dt = datetime.datetime(year, month, day, hour)
        date_str = dt.strftime("%Y-%m-%d-%H")
        resp = self._get(date_str)
        archive = self._decode_response(resp)
        return archive

    def _get(self, date: str) -> requests.Response:
        url = f"{BASE_URL}{date}.json.gz"
        logger.debug(f"Requesting url: {url}")
        return requests.get(url)

    def _decode_response(self, resp: requests.Response) -> Archive:
        return Archive.from_response(resp)

    def _validate_get(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        dt: Optional[datetime.datetime] = None,
    ):
        if dt is None:
            if year is None or month is None or day is None or hour is None:
                raise ValueError(
                    "must provide either dt or year, month, day, and hour"
                )
        if dt is not None:
            if (
                year is not None
                or month is not None
                or day is not None
                or hour is not None
            ):
                raise ValueError(
                    "cannot provide both dt and year, month, day, or hour"
                )
