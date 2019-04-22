import datetime as dt


class RateTrack:
    def __init__(self, maxrate=1, period=dt.timedelta(minutes=5)):
        self.maxrate = maxrate
        self.period = period
        self.rate_queue = []

    def timetoexpire(self):
        elapsed = dt.datetime.now() - self.rate_queue[0][0]
        return (self.period - elapsed).total_seconds()

    def update(self, request=None):
        out_req = {'waitSeconds': 0}
        if request is not None:
            self.rate_queue.append((dt.datetime.now(), request))
            if 'waitSeconds' in request:
                out_req = request

        # Filter expired requests from queue
        self.rate_queue = [req for req in self.rate_queue
                           if dt.datetime.now() - req[0] <= self.period]

        # Change wait time to prevent violating rate limit
        if len(self.rate_queue) > 0 and len(self.rate_queue) >= self.maxrate:
            # Allow time for at least one request to expire before adding more
            out_req['waitSeconds'] = self.timetoexpire()
        return out_req
