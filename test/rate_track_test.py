import datetime as dt

from freezegun import freeze_time

from src.rate_track import RateTrack


def test_update_returns_a_wait_time():
    paint_rate = RateTrack(dt.timedelta(minutes=5))
    result = paint_rate.update()
    assert 'waitSeconds' in result


def test_requests_are_stored_by_update():
    paint_rate = RateTrack(dt.timedelta(minutes=5))
    dummy_req = {}
    paint_rate.update(dummy_req)
    assert len(paint_rate.rate_queue) >= 1


def test_wait_time_changed_if_rate_saturated():
    paint_rate = RateTrack(dt.timedelta(minutes=5))
    dummy_req = {'waitSeconds': 0}
    result = paint_rate.update(dummy_req)
    assert result['waitSeconds'] > 0


def test_wait_time_if_rate_not_saturated():
    paint_rate = RateTrack(dt.timedelta(minutes=5), 2)
    dummy_req = {'waitSeconds': 0}
    result = paint_rate.update(dummy_req)
    assert result['waitSeconds'] == 0


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


def test_return_correct_wait_to_avoid_rate_voilation():
    paint_rate = RateTrack(dt.timedelta(minutes=2), 3)
    dummy_req = {'waitSeconds': 0}
    # nearly fill rate limit
    with freeze_time('12:00'):
        for x in range(2):
            paint_rate.update(dummy_req)
    # fill to limit 1 min later
    with freeze_time('12:01'):
        result = paint_rate.update(dummy_req)
        # return wait time that will allow at least one request to expire
        assert result['waitSeconds'] == 60


def test_handling_fractions_of_seconds():
    paint_rate = RateTrack(dt.timedelta(minutes=2), 3)
    dummy_req = {'waitSeconds': 0}
    # nearly fill rate limit
    with freeze_time('12:00'):
        for x in range(2):
            paint_rate.update(dummy_req)
    # fill to limit 1 min + 0.01 sec later
    with freeze_time('12:01:00.01'):
        result = paint_rate.update(dummy_req)
        # return wait time that will allow at least one request to expire
        assert result['waitSeconds'] == 59.99
