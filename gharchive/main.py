import datetime
from typing import Optional, Union, Tuple, Sequence

import requests
import gzip
import json

from gharchive.exc import NoArchiveForDateException, NoArchiveMatchingCriteraException
from gharchive.logger import logger
from gharchive.models import Archive
from gharchive.search import SearchDates

BASE_URL = "https://data.gharchive.org/"


class GHArchive:
    def __init__(self):
        pass

    def get(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        filters: Optional[Sequence[Tuple[str, Union[int, float, str]]]] = None,
    ) -> Archive:
        dates = SearchDates(start_date, end_date)
        archive = self._get_many_and_decode(dates, filters)
        return archive

    def _get_many_and_decode(
        self,
        dates: SearchDates,
        filters: Optional[Sequence[Tuple[str, Union[int, float, str]]]] = None,
    ) -> Archive:
        full_archive = None
        for i, search_date in enumerate(dates.strings):
            try:
                resp = self._get(str(search_date))
            except NoArchiveForDateException as e:
                logger.warning(str(e))
                continue
            archive = self._decode_response(resp, filters)
            if i == 0:
                full_archive = archive
            else:
                full_archive += archive

        if full_archive is None:
            raise NoArchiveMatchingCriteraException(
                f"Could not find any archives with search dates: {dates.strings}"
            )

        return full_archive

    def _get(self, date: str) -> requests.Response:
        url = f"{BASE_URL}{date}.json.gz"
        logger.debug(f"Requesting url: {url}")
        resp = requests.get(url)
        if resp.status_code != 200:
            raise NoArchiveForDateException(
                f"Got status code {resp.status_code} for date {date}. Content: {resp.text}"
            )
        return resp

    def _decode_response(
        self,
        resp: requests.Response,
        filters: Optional[Sequence[Tuple[str, Union[int, float, str]]]] = None,
    ) -> Archive:
        arch = Archive.from_response(resp)
        if filters:
            arch = arch.filter(filters)
        return arch
