from datetime import date
from decimal import Decimal

from dateutil.rrule import DAILY, rrule

from src.currency_exchange.constants import DecimalPrecission
from src.exceptions import DecimalError


def iter_days(start: date, end: date):
    for day in rrule(DAILY, dtstart=start, until=end):
        yield day


def round_decimal(amount: Decimal) -> Decimal:
    try:
        return amount.quantize(
            Decimal(10) ** - DecimalPrecission.DECIMAL_PLACES
        )
    except Exception:
        raise DecimalError("Invalid decimal operation")
