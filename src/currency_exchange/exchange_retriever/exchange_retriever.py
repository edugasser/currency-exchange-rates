import abc
from typing import List
from datetime import date

from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse


class ExchangeProvider(object):

    @abc.abstractmethod
    def get_latest(
        self,
        currency,
        exchanged_currencies: List[str]
    ) -> ExchangeResponse:
        pass

    @abc.abstractmethod
    def get_historical(
        self,
        currency,
        exchanged_currencies: List[str],
        valuation_date: date
    ) -> ExchangeResponse:
        pass


class ExchangeRetriver(object):

    def __init__(self, exchange_provider: ExchangeProvider):
        self.exchange_provider = exchange_provider

    def get(
        self,
        currency,
        exchanged_currencies: List[str],
        valuation_date: date
    ) -> ExchangeResponse:

        if valuation_date == date.today():
            response = self.exchange_provider.get_latest(currency, exchanged_currencies)  # noqa
        else:
            response = self.exchange_provider.get_historical(
                currency,
                exchanged_currencies,
                valuation_date
            )
        return response
