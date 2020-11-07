import abc
from datetime import date

from src.currency_exchange.constants import TypeProvider
from src.currency_exchange.exchange_retriever.exchange_provider import \
    ExchangeProvider
from src.currency_exchange.exchange_retriever.exchange_providers.fixer_io import \
    FixerProvider
from src.currency_exchange.exchange_retriever.exchange_providers.mock import \
    MockProvider
from src.exceptions import ExchangeCurrencyDoesNotExist, ExchangeProviderError


class CurrencyExchangeRepository:

    @abc.abstractmethod
    def get_active_provider(self):
        pass

    @abc.abstractmethod
    def get_all_currencies(self):
        pass

    @abc.abstractmethod
    def get(self, source_currency, exchanged_currency, valuation_date):
        pass

    @abc.abstractmethod
    def save(self, source_currency, exchanged_currency, rate):
        pass


class RetrieveCurrencyExchange(object):

    def __init__(self, exchange_repository: CurrencyExchangeRepository):
        self.exchange_repository = exchange_repository

    @staticmethod
    def get_exchange_rate_data(
            source_currency,
            exchanged_currency,
            valuation_date,
            provider
    ):
        exchange_response = ExchangeProvider(provider).get(
            source_currency,
            [exchanged_currency],
            valuation_date
        )
        if not exchange_response.success:
            raise ExchangeCurrencyDoesNotExist(
                "The {source_currency} doesn't has exchange for {exchanged_currency}"  # noqa
            )
        return exchange_response.rates[0].rate

    def obtain_active_provider(self):
        provider_code = self.exchange_repository.get_active_provider()

        if provider_code == TypeProvider.FIXER_IO:
            return FixerProvider()
        elif provider_code == TypeProvider.MOCK:
            return MockProvider()
        else:
            raise ExchangeProviderError(
                f"Invalid provider: {provider_code}"
            )

    def get(self, source_currency: str, exchanged_currency: str, valuation_date: date = None):  # noqa
        if not valuation_date:
            valuation_date = date.today()

        try:
            currency_rate = self.exchange_repository.get(
                source_currency,
                exchanged_currency,
                valuation_date
            )
        except ExchangeCurrencyDoesNotExist:
            provider = self.obtain_active_provider()
            currency_rate = self.get_exchange_rate_data(
                source_currency,
                exchanged_currency,
                valuation_date,
                provider
            )
        return currency_rate
