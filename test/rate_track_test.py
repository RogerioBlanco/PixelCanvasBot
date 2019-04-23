import datetime as dt

import pytest
from freezegun import freeze_time

from src.rate_track import RateTrack


def test_update_returns_a_wait_time():
    paint_rate = RateTrack(dt.timedelta(minutes=5))
    result = paint_rate.update()
    assert 'waitSeconds' in result


def test_requests_are_stored_by_update():
    paint_rate = RateTrack(dt.timedelta(minutes=5))
    dummy_req = {'waitSeconds': 0}
    paint_rate.update(dummy_req)
    assert len(paint_rate.rate_queue) == 1


@pytest.mark.parametrize("wait", [(1), (55.56), (300), (25200)])
def test_passthrough_if_not_saturated(wait):
    paint_rate = RateTrack(dt.timedelta(minutes=5), 2)
    dummy_req = {'waitSeconds': wait}
    result = paint_rate.update(dummy_req)
    assert result['waitSeconds'] == wait


@pytest.mark.parametrize("rate, expected", [(1, 300),  # saturated
                                            (2, 0)])  # not saturated
@freeze_time('12:00')
def test_saturation_wait_time(rate, expected):
    paint_rate = RateTrack(dt.timedelta(minutes=5), rate)
    dummy_req = {'waitSeconds': 0}
    result = paint_rate.update(dummy_req)
    assert result['waitSeconds'] == expected


def test_expired_requests_removed_on_update():
    paint_rate = RateTrack(dt.timedelta(seconds=30), 2)
    dummy_req = {'waitSeconds': 0}
    # add now
    paint_rate.update(dummy_req)
    assert len(paint_rate.rate_queue) == 1
    # update 1m later
    with freeze_time(lambda: dt.datetime.now() + dt.timedelta(minutes=1)):
        paint_rate.update()
    # stored req should have expired
    assert len(paint_rate.rate_queue) == 0


def test_valid_requests_not_removed_on_update():
    paint_rate = RateTrack(dt.timedelta(minutes=2), 6)
    dummy_req = {'waitSeconds': 0}
    # add 5 requests now
    for x in range(5):
        paint_rate.update(dummy_req)
    assert len(paint_rate.rate_queue) == 5
    # update 1m later
    with freeze_time(lambda: dt.datetime.now() + dt.timedelta(minutes=1)):
        paint_rate.update()
    # no reqs should expire
    assert len(paint_rate.rate_queue) == 5


def test_correct_amount_of_requests_after_some_expire():
    paint_rate = RateTrack(dt.timedelta(minutes=2), 6)
    dummy_req = {'waitSeconds': 0}
    # add 3 requests
    for x in range(3):
        paint_rate.update(dummy_req)
    # add 5 requests 130s later
    with freeze_time(lambda: dt.datetime.now() + dt.timedelta(minutes=2,
                                                              seconds=10)):
        for x in range(5):
            paint_rate.update(dummy_req)
        # 3 requests should expire, for total 5 remaining
        assert len(paint_rate.rate_queue) == 5


@pytest.mark.parametrize("t1, t2, expected",
                         [('12:00', '12:01', 60),  # basic
                          ('12:00', '12:01:00.01', 59.99)])  # fractional sec
def test_avoid_rate_violations(t1, t2, expected):
    paint_rate = RateTrack(dt.timedelta(minutes=2), 3)
    dummy_req = {'waitSeconds': 0}
    # nearly fill
    with freeze_time(t1):
        for x in range(2):
            paint_rate.update(dummy_req)
    # fill to limit at t2
    with freeze_time(t2):
        result = paint_rate.update(dummy_req)
        # return wait time that will allow at least one request to expire
        assert result['waitSeconds'] == expected
