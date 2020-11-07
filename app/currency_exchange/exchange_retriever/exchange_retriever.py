import abc
from typing import List

from app.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse


class ExchangeProvider(object):

    @abc.abstractmethod
    def get_latest(self,  currencies: List[str]) -> ExchangeResponse:
        pass

    @abc.abstractmethod
    def get_historical(self,  currencies: List[str]) -> ExchangeResponse:
        pass


class ExchangeRetriver(object):

    def __init__(self, exchange_provider: ExchangeProvider):
        self.exchange_provider = exchange_provider

    def run(self):
        pass
