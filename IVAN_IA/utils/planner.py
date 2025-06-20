import datetime
from typing import List, Tuple, Dict, Set
from config import REVISION_OFFSETS
from utils.helpers import shift_to_previous_available

def compute_revision_sessions(
    subject_id: int,
    exam_date: datetime.date,
    available_days: Set[str]
) -> List[Tuple[int, datetime.date, str]]:

    sessions: List[Tuple[int, datetime.date, str]] = []
    for offset in REVISION_OFFSETS:
        target_date = exam_date - datetime.timedelta(days=offset)
        adjusted_date = shift_to_previous_available(target_date, available_days)
        if adjusted_date:
            label = f"{offset} days before exam"
            sessions.append((subject_id, adjusted_date, label))
    return sessions

def aggregate_sessions(
    all_sessions: List[Tuple[int, datetime.date, str]]) -> Dict[str, List[Tuple[int, str]]]:

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    calendar: Dict[str, List[Tuple[int, str]]] = {day: [] for day in weekdays}

    for subject_id, session_date, label in all_sessions:
        weekday = session_date.strftime('%A')
        if weekday in calendar:
            calendar[weekday].append((subject_id, label))

    return calendar
