import abc
from datetime import date
from typing import List

from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse
from src.logger import logger, _


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
            logger.info(
                _("Exchange provider: latest",
                  valuation_date=valuation_date,
                  response=response))
        else:
            logger.info(_("Exchange provider: historical", valuation_date=valuation_date))  # noqa
            response = self.exchange_provider.get_historical(
                currency,
                exchanged_currencies,
                valuation_date
            )
            logger.info(
                _("Exchange provider: latest",
                  valuation_date=valuation_date,
                  response=response))
        return response
