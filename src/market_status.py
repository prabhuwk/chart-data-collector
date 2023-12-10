from datetime import datetime, time
from enum import Enum


class TradingHours(Enum):
    START_TIME = time(9, 15)
    END_TIME = time(23, 59)


class MarketStatus:
    def __init__(self) -> None:
        self._time = datetime.now()
        self.closed = self._closed()

    def _weekday(self):
        return self._time.weekday() >= 5

    def _closed(self):
        return (
            self._weekday()
            and TradingHours.START_TIME.value
            <= self._time.time()
            <= TradingHours.END_TIME.value
        )
