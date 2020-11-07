from datetime import date
from typing import List

from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse, CurrencyRate
from src.currency_exchange.exchange_retriever.exchange_retriever import \
    ExchangeProvider


class MockProvider(ExchangeProvider):

    @staticmethod
    def build_response(success, _date, base, exchange_rates):
        rates = []
        for currency, ratio in exchange_rates:
            rates.append(CurrencyRate(currency, ratio))

        return ExchangeResponse(
            success,
            _date,
            base,
            rates
        )

    def get_latest(self, currencies: List[str]) -> ExchangeResponse:
        return self.build_response(True, date.today(), "EUR", {"USD": 1.0})

    def get_historical(
            self,
            currencies: List[str],
            valuation_date: date) -> ExchangeResponse:
        return self.build_response(True, date.today(), "EUR", {"USD": 1.0})
