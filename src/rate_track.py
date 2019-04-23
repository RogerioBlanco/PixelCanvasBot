import datetime as dt
from collections import deque


class RateTrack:
    def __init__(self, period, maxrate=1):
        self.maxrate = int(maxrate)
        self.period = period
        self.rate_queue = deque()

    def getrelief(self):
        # Index of request that we need to expire
        pressure = self.maxrate - len(self.rate_queue) - 1
        elapsed = dt.datetime.now() - self.rate_queue[pressure][0]
        return (self.period - elapsed).total_seconds()

    def update(self, request=None):
        out_req = {'waitSeconds': 0}
        if request is not None:
            self.rate_queue.appendleft((dt.datetime.now(), dict(request)))
            if 'waitSeconds' in request:
                out_req = dict(request)

        # Filter expired requests from queue
        self.rate_queue = deque([req for req in self.rate_queue
                                 if dt.datetime.now() - req[0]
                                 <= self.period])

        # If queue is full
        if len(self.rate_queue) > 0 and len(self.rate_queue) >= self.maxrate:
            # Allow relief until there's space for a new request
            out_req['waitSeconds'] = max(self.getrelief(),
                                         out_req['waitSeconds'])
        return out_req
