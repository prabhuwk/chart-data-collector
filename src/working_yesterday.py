from datetime import date, datetime, timedelta
from functools import cached_property
from typing import List

from utils import read_yaml_file


class WorkingYesterday:
    def __init__(self, holidays_file: str) -> None:
        self.holidays_file = holidays_file
        self.today = datetime.today().date()
        self.holidays = self._holidays()

    def _holidays(self) -> List[date]:
        holidays = read_yaml_file(self.holidays_file)
        return [
            datetime.strptime(holiday, "%d-%b-%Y").date()
            for holiday in holidays[self.today.year]
        ]

    def holiday(self, date_: date) -> bool:
        return True if date_ in self.holidays else False

    @cached_property
    def get(self) -> date:
        yesterday = self.today - timedelta(days=1)
        while self.holiday(yesterday) or yesterday.weekday() in (5, 6):
            yesterday = yesterday - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")
