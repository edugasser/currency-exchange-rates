from src.currency_exchange.models import CurrencyExchangeRate, Provider, \
    Currency
from src.currency_exchange.use_cases.retrieve_currency_exchange import \
    CurrencyExchangeRepository
from src.exceptions import ExchangeProviderError, ExchangeCurrencyDoesNotExist


class CurrencyExchangeRepositoryDB(CurrencyExchangeRepository):

    def get_all_currencies(self):
        return Currency.objects.all().values_list('code', flat=True)

    def get_active_provider(self):
        provider = Provider.objects.order_by('order').first()
        if not provider:
            raise ExchangeProviderError(f"Provider {provider} not exists in db")  # noqa
        return provider.code

    def get(self, source_currency, exchanged_currency, valuation_date):
        try:
            exchange = CurrencyExchangeRate.objects.get(
                source_currency__code=source_currency,
                exchanged_currency__code=exchanged_currency,
                valuation_date=valuation_date
            )
            return exchange.rate_value
        except CurrencyExchangeRate.DoesNotExist:
            raise ExchangeCurrencyDoesNotExist(
                f"Exchanged currency doesn't exist {source_currency} to {exchanged_currency}"  # noqa
            )


currency_exchange_repository = CurrencyExchangeRepositoryDB()
