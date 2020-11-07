import date
from typing import List
from dataclasses import dataclass


@dataclass
class CurrencyRate:
    currency: str
    rate: float


@dataclass
class ExchangeResponse:
    success: str
    exchange_date: date
    base_currency: str
    rates: List[CurrencyRate]
