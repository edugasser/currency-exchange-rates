from src.currency_exchange.constants import TypeProvider
from src.currency_exchange.exchange_retriever.exchange_providers.fixer_io import \
    FixerProvider
from src.currency_exchange.exchange_retriever.exchange_providers.mock import \
    MockProvider
from src.currency_exchange.repository import CurrencyExchangeRepository
from src.exceptions import ExchangeProviderError


class ObtainActiveProvider(object):

    def __init__(self, exchange_repository: CurrencyExchangeRepository):
        self.exchange_repository = exchange_repository

    def get(self):
        provider_code = self.exchange_repository.get_active_provider()

        if provider_code == TypeProvider.FIXER_IO:
            return FixerProvider()
        elif provider_code == TypeProvider.MOCK:
            return MockProvider()
        else:
            raise ExchangeProviderError(
                f"Invalid provider: {provider_code}"
            )
