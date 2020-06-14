import datetime
import itertools
from typing import Optional, Tuple, Union, List

import pandas as pd

SUPPORTED_BEGIN_YEAR = 2015


class SearchDates:
    strings: List[str]

    def __init__(
        self,
        start_date: str,
        end_date: Optional[str] = None
    ):
        if end_date is None:
            end_date = start_date
        self.start_date = start_date
        self.end_date = end_date
        self.strings = self.make_strs()

    def make_strs(self) -> List[str]:
        dates = pd.date_range(start=self.start_date, end=self.end_date, freq='h')
        date_strs = [_date_to_str(date) for date in dates]
        return date_strs


def _date_to_str(date: pd.Timestamp):
    mdy = date.strftime("%Y-%m-%d")
    if date.hour == 0:
        h = '0'
    else:
        h = date.strftime("%H").lstrip("0")
    return f'{mdy}-{h}'


def _zero_pad(num: int) -> str:
    num_str = str(num)
    if len(num_str) > 1:
        return num_str
    elif len(num_str) == 1:
        return f"0{num}"
    else:
        raise ValueError(f"invalid num: {num}")
