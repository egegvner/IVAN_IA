import datetime
from typing import Set, Optional

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def date_to_weekday(date: datetime.date) -> str:
    return date.strftime('%A')

def shift_to_previous_available(date: datetime.date, available_days: Set[str]) -> Optional[datetime.date]:
    if date_to_weekday(date) in available_days:
        return date

    for i in range(1, 7):
        prev_date = date - datetime.timedelta(days=i)
        if date_to_weekday(prev_date) in available_days:
            return prev_date

    return None

def format_date(date: datetime.date, fmt: str = '%Y-%m-%d') -> str:
    return date.strftime(fmt)