import abc

from src.currency_exchange.constants import TypeProvider
from src.currency_exchange.exchange_retriever.exchange_providers.fixer_io import \
    FixerProvider
from src.currency_exchange.exchange_retriever.exchange_providers.mock import \
    MockProvider
from src.currency_exchange.exchange_retriever.exchange_retriever import \
    ExchangeRetriver
from src.exceptions import ExchangeCurrencyDoesNotExist, ExchangeProviderError


class CurrencyExchangeRepository:

    @abc.abstractmethod
    def get_active_provider(self):
        pass

    @abc.abstractmethod
    def get(self, source_currency, exchanged_currency, valuation_date):
        pass


class RetrieveExchange(object):

    def __init__(self, exchange_repository: CurrencyExchangeRepository):
        self.exchange_repository = exchange_repository

    def obtain_active_provider(self):
        provider_code = self.exchange_repository.get_active_provider()

        if provider_code == TypeProvider.FIXER_IO:
            return FixerProvider()
        elif provider_code == TypeProvider.MOCK:
            return MockProvider()
        else:
            raise ExchangeProviderError(
                f"Invalid active provider: {provider_code}"
            )

    def get(self, source_currency, exchanged_currency, valuation_date):
        try:
            currency_rate = self.exchange_repository.get(
                source_currency,
                exchanged_currency,
                valuation_date
            )
        except ExchangeCurrencyDoesNotExist:
            provider = self.obtain_active_provider()
            currency_rate = get_exchange_rate_data(
                source_currency,
                exchanged_currency,
                valuation_date,
                provider
            )
        return currency_rate


def get_exchange_rate_data(
        source_currency,
        exchanged_currency,
        valuation_date,
        provider
        ):
    exchange_response = ExchangeRetriver(provider).get(
        source_currency,
        [exchanged_currency],
        valuation_date
    )
    if not exchange_response.success:
        raise ExchangeCurrencyDoesNotExist(
            "The {source_currency} doesn't has exchange for {exchanged_currency}"  # noqa
        )
    return exchange_response.rates[0].rate
