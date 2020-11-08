from datetime import date

from dateutil.rrule import DAILY, rrule


def iter_days(start: date, end: date):
    for day in rrule(DAILY, dtstart=start, until=end):
        yield day
