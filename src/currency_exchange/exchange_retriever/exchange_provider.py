import abc
from datetime import date
from typing import List

from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse


class ExchangeProviderInterface(object):

    @abc.abstractmethod
    def get_latest(
        self,
        currency: str,
        exchanged_currencies: List[str]
    ) -> ExchangeResponse:
        pass

    @abc.abstractmethod
    def get_historical(
        self,
        currency: str,
        exchanged_currencies: List[str],
        valuation_date: date
    ) -> ExchangeResponse:
        pass


class ExchangeProvider(object):

    def __init__(self, exchange_provider: ExchangeProviderInterface):
        self.exchange_provider = exchange_provider

    def get(
        self,
        currency: str,
        exchanged_currencies: List[str],
        valuation_date: date
    ) -> ExchangeResponse:

        if valuation_date == date.today():
            response = self.exchange_provider.get_latest(
                currency,
                exchanged_currencies
            )
        else:
            response = self.exchange_provider.get_historical(
                currency,
                exchanged_currencies,
                valuation_date
            )

        return response
