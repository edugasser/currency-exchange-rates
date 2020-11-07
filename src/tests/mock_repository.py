from src.currency_exchange.exchange_retriever.exchange_providers.mock import \
    MockProvider
from src.currency_exchange.use_cases.retrieve_exchange import \
    CurrencyExchangeRepository


class MockRepository(CurrencyExchangeRepository):

    def get_active_provider(self):
        return MockProvider()

    def get(self, source_currency, exchanged_currency, valuation_date):
        return 10.

    def get_all_currencies(self):
        return ["EUR", "USD"]

    def save(self, source_currency, exchanged_currency, rate):
        pass
