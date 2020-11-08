from datetime import date
from decimal import Decimal

from dateutil.rrule import DAILY, rrule

from src.currency_exchange.constants import DecimalPrecission


def iter_days(start: date, end: date):
    for day in rrule(DAILY, dtstart=start, until=end):
        yield day


def round_decimal(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal(10) ** - DecimalPrecission.DECIMAL_PLACES)
