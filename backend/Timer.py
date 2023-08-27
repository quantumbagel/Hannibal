import time


class Timer:
    def __init__(self, start_time=time.time(), allowed=250) -> None:
        """
        Initialize the Timer.
        :param start_time: The epoch time when the timer began
        :param allowed: the time for the timer to expire
        """
        self.start_time = start_time
        self.allowed = allowed

    @property
    def ms_remaining(self) -> float:
        """
        The dynamic ms_remaining property
        :return: the ms remaining
        """
        return self.allowed - (time.time()-self.start_time) * 100
