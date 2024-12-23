from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class RetryStrategy(ABC):
    @abstractmethod
    def next_retry_time(self, attempts: int) -> datetime:
        pass

class ExponentialBackoff(RetryStrategy):
    def __init__(self, base_delay: int = 5):
        self.base_delay = base_delay

    def next_retry_time(self, attempts: int) -> datetime:
        delay = self.base_delay * (2 ** (attempts - 1))
        return datetime.utcnow() + timedelta(seconds=delay)

class LinearBackoff(RetryStrategy):
    def __init__(self, delay: int = 300):  # 5 minutes
        self.delay = delay

    def next_retry_time(self, attempts: int) -> datetime:
        return datetime.utcnow() + timedelta(seconds=self.delay) 