from src.currency_exchange.models import CurrencyExchangeRate, Provider, \
    Currency
from src.currency_exchange.use_cases.retrieve_exchange import \
    CurrencyExchangeRepository
from src.exceptions import ExchangeProviderError


class CurrencyExchangeRepositoryDB(CurrencyExchangeRepository):

    def get_all_currencies(self):
        return Currency.objects.all().values_list('code', flat=True)

    def get_active_provider(self):
        provider = Provider.objects.order_by('order').first()
        if not provider:
            raise ExchangeProviderError(f"Provider {provider} not exists in db")  # noqa
        return provider.code

    def get(self, source_currency, exchanged_currency, valuation_date):
        return CurrencyExchangeRate.objects.all()


currency_exchange_repository = CurrencyExchangeRepositoryDB()
