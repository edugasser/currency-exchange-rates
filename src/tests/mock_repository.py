from decimal import Decimal

from src.currency_exchange.constants import TypeProvider
from src.currency_exchange.repository import CurrencyExchangeRepository


class MockRepository(CurrencyExchangeRepository):

    def get_active_provider(self):
        return TypeProvider.MOCK

    def get(self, source_currency, exchanged_currency, valuation_date):
        return Decimal(10)

    def get_all_currencies(self):
        return ["EUR", "USD"]

    def save(self, source_currency, exchanged_currency, rate):
        pass
