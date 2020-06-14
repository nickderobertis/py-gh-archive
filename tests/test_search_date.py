import datetime

from gharchive.search import SearchDates


def test_create_with_begin_only():
    date = SearchDates(datetime.datetime(2020, 1, 1, 5))
    assert date.strings == ["2020-01-01-5"]


def test_create_with_begin_and_end():
    date = SearchDates(
        datetime.datetime(2020, 1, 1, 5), datetime.datetime(2020, 1, 1, 10),
    )
    assert date.strings == [
        "2020-01-01-5",
        "2020-01-01-6",
        "2020-01-01-7",
        "2020-01-01-8",
        "2020-01-01-9",
        "2020-01-01-10",
    ]
