import datetime as dt
from collections import deque


class RateTrack:
    def __init__(self, period, maxrate=1):
        self.maxrate = maxrate
        self.period = period
        self.rate_queue = deque()

    def timetoexpire(self):
        elapsed = dt.datetime.now() - self.rate_queue[-1][0]
        return (self.period - elapsed).total_seconds()

    def update(self, request=None):
        out_req = {'waitSeconds': 0}
        if request is not None:
            self.rate_queue.appendleft((dt.datetime.now(), request))
            if 'waitSeconds' in request:
                out_req = request

        # Filter expired requests from queue
        self.rate_queue = deque([req for req in self.rate_queue
                                 if dt.datetime.now() - req[0]
                                 <= self.period])

        # Change wait time to prevent violating rate limit
        if len(self.rate_queue) > 0 and len(self.rate_queue) >= self.maxrate:
            # Allow time for at least one request to expire before adding more
            out_req['waitSeconds'] = max(self.timetoexpire(),
                                         out_req['waitSeconds'])
        return out_req
