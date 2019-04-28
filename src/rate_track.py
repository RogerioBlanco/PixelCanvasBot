import datetime as dt
from collections import deque
from copy import deepcopy
import math


class RateTrack:
    def __init__(self, period, maxrate=1):
        self.maxrate = int(maxrate)
        self.period = period
        self.rate_queue = deque()
        self.genesis = dt.datetime.now()

    def ppm(self):
        self.update()
        print(len(self.rate_queue))
        sincegenesis = dt.datetime.now() - self.genesis
        # Return infinity if no time since genesis
        if sincegenesis.total_seconds() == 0:
            return math.inf
        k_period = min(sincegenesis, self.period)
        k_minutes = k_period.total_seconds() / 60
        return len(self.rate_queue) / k_minutes

    @property
    def relief(self):
        # Index of request that we need to expire
        pressure = self.maxrate - len(self.rate_queue) - 1
        elapsed = dt.datetime.now() - self.rate_queue[pressure][0]
        return (self.period - elapsed).total_seconds()

    def update(self, req=None):
        out_req = {'waitSeconds': 0}
        if req is not None:
            self.rate_queue.appendleft((dt.datetime.now(), deepcopy(req)))
            if type(req) is dict and 'waitSeconds' in req:
                out_req = dict(req)

        # Filter expired requests from queue
        self.rate_queue = deque([req for req in self.rate_queue
                                 if dt.datetime.now() - req[0]
                                 <= self.period])

        # If queue is full
        if len(self.rate_queue) > 0 and len(self.rate_queue) >= self.maxrate:
            if type(out_req) is dict:
                # Allow relief until there's space for a new request
                out_req['waitSeconds'] = max(self.relief,
                                             out_req['waitSeconds'])
        return out_req
