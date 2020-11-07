from datetime import date
from typing import List
from dataclasses import dataclass


@dataclass
class CurrencyRate:
    currency: str
    rate: float


@dataclass
class ExchangeResponse:
    success: bool
    exchange_date: date
    base_currency: str
    rates: List[CurrencyRate]
