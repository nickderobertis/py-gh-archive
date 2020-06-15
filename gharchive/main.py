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
    """
    Main class for getting Github Archive data.

    :Examples:

        >>> from gharchive import GHArchive
        >>> gh = GHArchive()
        ...
        >>> data = gh.get('6/8/2020', '6/10/2020', filters=[
        >>>     ('repo.name', 'bitcoin/bitcoin'),
        >>>     ('type', 'WatchEvent')
        >>> ])
    """

    def get(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        filters: Optional[Sequence[Tuple[str, Union[int, float, str]]]] = None,
    ) -> Archive:
        """
        Get data from the Github Archive

        :param start_date: string of date or datetime to start collection
        :param end_date: string of date or datetime to end collection, defaults to
        the same as start date
        :param filters: filters in the format of two-element tuples for which
        the first element is the . separated path to look up a value from the
        Archive object and the second is a value which it should be equal to
        :return: Archive object containing Github Archive data

        :Examples:

                >>> from gharchive import GHArchive
                >>> gh = GHArchive()
                ...
                >>> data = gh.get('6/8/2020', '6/10/2020', filters=[
                >>>     ('repo.name', 'bitcoin/bitcoin'),
                >>>     ('type', 'WatchEvent')
                >>> ])
        """
        dates = SearchDates(start_date, end_date)
        archive = self._get_many_and_decode(dates, filters)
        return archive

    def _get_many_and_decode(
        self,
        dates: SearchDates,
        filters: Optional[Sequence[Tuple[str, Union[int, float, str]]]] = None,
    ) -> Archive:
        full_archive = Archive([])
        for search_date in dates.strings:
            try:
                resp = self._get(str(search_date))
            except NoArchiveForDateException as e:
                logger.warning(str(e))
                continue
            archive = self._decode_response(resp, filters)
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
