from datetime import date
from typing import List
import random

from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse, CurrencyRate
from src.currency_exchange.exchange_retriever.exchange_retriever import \
    ExchangeProvider


class MockProvider(ExchangeProvider):

    @staticmethod
    def build_response(success, _date, base, exchange_rates):
        rates = []
        for currency, ratio in exchange_rates.items():
            rates.append(CurrencyRate(currency, ratio))

        return ExchangeResponse(
            success,
            _date,
            base,
            rates
        )

    @staticmethod
    def get_random_rates(exchanged_currencies):
        rates = {}
        for exchanged_currency in exchanged_currencies:
            rates[exchanged_currency] = random.random()
        return rates

    def get_latest(
        self,
        currency: str,
        exchanged_currencies: List[str]
    ) -> ExchangeResponse:
        rates = self.get_random_rates(exchanged_currencies)
        return self.build_response(True, date.today(), currency, rates)

    def get_historical(
            self,
            currency: str,
            exchanged_currencies: List[str],
            valuation_date: date) -> ExchangeResponse:
        rates = self.get_random_rates(exchanged_currencies)
        return self.build_response(True, valuation_date, currency, rates)
