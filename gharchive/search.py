import datetime
import itertools
from typing import Optional, Tuple, Union, List

SUPPORTED_BEGIN_YEAR = 2015


class SearchDates:
    strings: List[str]

    def __init__(
        self,
        year: Optional[Union[int, Tuple[int, int]]] = None,
        month: Optional[Union[int, Tuple[int, int]]] = None,
        day: Optional[Union[int, Tuple[int, int]]] = None,
        hour: Optional[Union[int, Tuple[int, int]]] = None,
        dt: Optional[datetime.datetime] = None,
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.dt = dt
        self._validate()
        self.strings = self.make_strs()

    def _validate(self):
        if (
            self.dt is None
            and self.year is None
            and self.month is None
            and self.day is None
            and self.hour is None
        ):
            raise ValueError("must provide either dt, year, month, day, or hour")
        if self.dt is not None:
            if (
                self.year is not None
                or self.month is not None
                or self.day is not None
                or self.hour is not None
            ):
                raise ValueError("cannot provide both dt and year, month, day, or hour")

    def make_strs(self) -> List[str]:
        if self.dt is not None:
            # Month and day should have leading zeroes but not hour
            return [
                self.dt.strftime("%Y-%m-%d") + "-" + self.dt.strftime("%H").strip("0")
            ]

        today = datetime.datetime.today()

        default_tuples = dict(
            year=(SUPPORTED_BEGIN_YEAR, today.year),
            month=("01", 12),
            day=("01", 31),
            hour=(0, 23),
        )

        for attr in ["year", "month", "day", "hour"]:
            self_value = getattr(self, attr, None)
            if self_value is None:
                default_value = default_tuples[attr]
                setattr(self, attr, default_value)
            elif not isinstance(self_value, tuple):
                setattr(self, attr, (self_value,))

            # Now should be tuple of begin and end. Now convert to tuple of each, e.g. (1, 3) -> (1, 2, 3)
            self_value = getattr(self, attr)
            if len(self_value) != 2:
                continue
            bot, top = self_value
            full_value = tuple([i for i in range(int(bot), int(top) + 1)])
            if attr != "hour":
                full_value = tuple([_zero_pad(num) for num in full_value])
            setattr(self, attr, full_value)

        all_strings = []
        for year, month, day, hour in itertools.product(
            self.year, self.month, self.day, self.hour
        ):
            year_str, month_str, day_str = [
                _zero_pad(num) for num in [year, month, day]
            ]
            hour_str = str(hour)
            full_str = f"{year_str}-{month_str}-{day_str}-{hour_str}"
            all_strings.append(full_str)

        return all_strings


def _from_to_str(t_from: Union[str, int], t_to: Union[str, int]) -> str:
    return f"{{{t_from}..{t_to}}}"


def _zero_pad(num: int) -> str:
    num_str = str(num)
    if len(num_str) > 1:
        return num_str
    elif len(num_str) == 1:
        return f"0{num}"
    else:
        raise ValueError(f"invalid num: {num}")
