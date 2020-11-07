import abc

from app.currency_exchange.models import CurrencyExchangeRate, Provider
from app.exceptions import ExchangeProviderError


class CurrencyExchangeRepository:

    @abc.abstractmethod
    def get_active_provider(self):
        pass

    @abc.abstractmethod
    def get(self, source_currency, exchanged_currency, valuation_date):
        pass


class CurrencyExchangeRepositoryDB(CurrencyExchangeRepository):

    def get_active_provider(self):
        provider = Provider.objects.order_by('order').first()
        if not provider:
            raise ExchangeProviderError(f"Provider {provider} not exists in db")  # noqa
        return provider.code

    def get(self, source_currency, exchanged_currency, valuation_date):
        return CurrencyExchangeRate.objects.all()
