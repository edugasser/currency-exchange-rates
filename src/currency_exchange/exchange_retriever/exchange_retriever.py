import abc
from typing import List
from datetime import date

from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse


class ExchangeProvider(object):

    @abc.abstractmethod
    def get_latest(self, currency, exchanged_currencies: List[str]) -> ExchangeResponse:  # noqa
        pass

    @abc.abstractmethod
    def get_historical(self,  currency, exchanged_currencies: List[str], valuation_date: date) -> ExchangeResponse:  # noqa
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
            # NOTE: Could it be possible that one provider doesn't has this
            # feature or some limitations on the days in the past of what you
            # can request. In that cases, an empty response will be given.
            response = self.exchange_provider.get_historical(
                currency,
                exchanged_currencies,
                valuation_date
            )
        return response
