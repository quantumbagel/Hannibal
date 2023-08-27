import time


class Timer:
    def __init__(self, start_time, allowed):
        self.start_time = start_time
        self.allowed = allowed

    @property
    def ms_remaining(self):
        return self.allowed - (time.time()-self.start_time) * 100
