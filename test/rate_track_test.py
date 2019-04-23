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


@pytest.mark.parametrize("in_time, expected",
                         # Relief time is 300
                         [(25200, 25200),
                          (299, 300),
                          (300, 300),
                          (20, 300)])
@freeze_time('12:00')
def test_wait_only_changed_if_relief_time_larger(in_time, expected):
    paint_rate = RateTrack(dt.timedelta(seconds=300), 1)
    dummy_req = {'waitSeconds': in_time}  # 7 hour timer
    result = paint_rate.update(dummy_req)
    assert result['waitSeconds'] == expected


@pytest.mark.parametrize("time, range1, range2, expected_len",
                         [('12:03', 1, 1, 1),
                          ('12:01', 3, 0, 3),
                          ('12:03', 3, 5, 5)])
def test_requests_expire_correctly(time, range1, range2, expected_len):
    paint_rate = RateTrack(dt.timedelta(minutes=2))
    dummy_req = {'waitSeconds': 0}
    # Add first batch of requests
    with freeze_time('12:00'):
        for x in range(range1):
            paint_rate.update(dummy_req)
    # Add second batch
    with freeze_time(time):
        for x in range(range2):
            paint_rate.update(dummy_req)
        paint_rate.update()
    assert len(paint_rate.rate_queue) == expected_len


@pytest.mark.parametrize("time, expected",
                         [('12:01', 60),  # basic
                          ('12:01:00.01', 59.99)])  # fractional sec
def test_update_allows_appropriate_relief_time(time, expected):
    paint_rate = RateTrack(dt.timedelta(minutes=2), 3)
    dummy_req = {'waitSeconds': 0}
    # nearly fill
    with freeze_time('12:00'):
        for x in range(2):
            paint_rate.update(dummy_req)
    # fill to limit at t2
    with freeze_time(time):
        result = paint_rate.update(dummy_req)
        # return wait time that will allow at least one request to expire
        assert result['waitSeconds'] == expected


def test_correct_relief_for_rate_overflow():
    paint_rate = RateTrack(dt.timedelta(minutes=5), 2)
    dummy_req = {'waitSeconds': 0}
    # Fill past rate limit
    with freeze_time('12:00'):
        paint_rate.update(dummy_req)
    with freeze_time('12:01'):
        paint_rate.update(dummy_req)
    with freeze_time('12:02'):
        paint_rate.update(dummy_req)
    with freeze_time('12:03'):
        result = paint_rate.update(dummy_req)
        # Relief time should allow room for one new request
        assert result['waitSeconds'] == 4 * 60


@pytest.mark.parametrize("maxrate",
                         [(10), (37.5)])
def test_prevent_rate_limit_vioation(maxrate):
    paint_rate = RateTrack(dt.timedelta(minutes=2), maxrate)
    dummy_req = {'waitSeconds': 0}
    with freeze_time('12:00'):
        for x in range(int(maxrate) - 1):
            paint_rate.update(dummy_req)
    with freeze_time('12:01'):
        result = paint_rate.update(dummy_req)
        assert result['waitSeconds'] == 60
