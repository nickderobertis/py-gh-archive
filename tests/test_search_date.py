import datetime

from gharchive.search import SearchDates


def test_create_with_dt():
    date = SearchDates(dt=datetime.datetime(2020, 1, 1, 5))
    assert date.strings == ["2020-01-01-5"]


def test_create_with_all_int():
    date = SearchDates(2020, 1, 1, 5)
    assert date.strings == ["2020-01-01-5"]


def test_create_no_year():
    date = SearchDates(month=1, day=1, hour=5)
    assert date.strings == [
        "2015-01-01-5",
        "2016-01-01-5",
        "2017-01-01-5",
        "2018-01-01-5",
        "2019-01-01-5",
        "2020-01-01-5",
    ]


def test_create_no_month():
    date = SearchDates(year=2020, day=1, hour=5)
    assert date.strings == [
        "2020-01-01-5",
        "2020-02-01-5",
        "2020-03-01-5",
        "2020-04-01-5",
        "2020-05-01-5",
        "2020-06-01-5",
        "2020-07-01-5",
        "2020-08-01-5",
        "2020-09-01-5",
        "2020-10-01-5",
        "2020-11-01-5",
        "2020-12-01-5",
    ]


def test_create_no_day():
    date = SearchDates(year=2020, month=1, hour=5)
    assert date.strings == [
        "2020-01-01-5",
        "2020-01-02-5",
        "2020-01-03-5",
        "2020-01-04-5",
        "2020-01-05-5",
        "2020-01-06-5",
        "2020-01-07-5",
        "2020-01-08-5",
        "2020-01-09-5",
        "2020-01-10-5",
        "2020-01-11-5",
        "2020-01-12-5",
        "2020-01-13-5",
        "2020-01-14-5",
        "2020-01-15-5",
        "2020-01-16-5",
        "2020-01-17-5",
        "2020-01-18-5",
        "2020-01-19-5",
        "2020-01-20-5",
        "2020-01-21-5",
        "2020-01-22-5",
        "2020-01-23-5",
        "2020-01-24-5",
        "2020-01-25-5",
        "2020-01-26-5",
        "2020-01-27-5",
        "2020-01-28-5",
        "2020-01-29-5",
        "2020-01-30-5",
        "2020-01-31-5",
    ]


def test_create_no_hour():
    date = SearchDates(year=2020, month=1, day=1)
    assert date.strings == [
        "2020-01-01-0",
        "2020-01-01-1",
        "2020-01-01-2",
        "2020-01-01-3",
        "2020-01-01-4",
        "2020-01-01-5",
        "2020-01-01-6",
        "2020-01-01-7",
        "2020-01-01-8",
        "2020-01-01-9",
        "2020-01-01-10",
        "2020-01-01-11",
        "2020-01-01-12",
        "2020-01-01-13",
        "2020-01-01-14",
        "2020-01-01-15",
        "2020-01-01-16",
        "2020-01-01-17",
        "2020-01-01-18",
        "2020-01-01-19",
        "2020-01-01-20",
        "2020-01-01-21",
        "2020-01-01-22",
        "2020-01-01-23",
    ]


def test_create_with_year_tuple():
    date = SearchDates(year=(2018, 2019), month=1, day=1, hour=5)
    assert date.strings == ["2018-01-01-5", "2019-01-01-5"]


def test_create_with_month_tuple():
    date = SearchDates(year=2020, month=(2, 3), day=1, hour=5)
    assert date.strings == ["2020-02-01-5", "2020-03-01-5"]


def test_create_with_day_tuple():
    date = SearchDates(year=2020, month=1, day=(7, 15), hour=5)
    assert date.strings == [
        "2020-01-07-5",
        "2020-01-08-5",
        "2020-01-09-5",
        "2020-01-10-5",
        "2020-01-11-5",
        "2020-01-12-5",
        "2020-01-13-5",
        "2020-01-14-5",
        "2020-01-15-5",
    ]


def test_create_with_hour_tuple():
    date = SearchDates(year=2020, month=1, day=1, hour=(9, 11))
    assert date.strings == ["2020-01-01-9", "2020-01-01-10", "2020-01-01-11"]
