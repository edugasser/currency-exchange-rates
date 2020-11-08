import abc
from datetime import date
from decimal import Decimal

from django.forms import ModelForm

from src.currency_exchange.models import CurrencyExchangeRate, Provider, \
    Currency
from src.exceptions import ExchangeProviderError, ExchangeCurrencyDoesNotExist, \
    ExchangeCurrencyError


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
    def save(
        self,
        source_currency: str,
        exchange_currency: str,
        rate_value: Decimal,
        valuation_date: date
    ):
        pass


class CurrencyExchangeRateForm(ModelForm):

    def clean_source_currency(self):
        return Currency.objects.get(code=self.cleaned_data.get('source_currency'))

    def clean_exchange_currency(self):
        return Currency.objects.get(code=self.cleaned_data.get('exchange_currency'))

    class Meta:
        model = CurrencyExchangeRate
        fields = ("source_currency", "exchanged_currency", "valuation_date", "rate_value")


class CurrencyExchangeRepositoryDB(CurrencyExchangeRepository):

    def get_all_currencies(self):
        return Currency.objects.all().values_list('code', flat=True)

    def get_active_provider(self):
        try:
            provider = Provider.objects.get(default=True)
        except (Provider.DoesNotExist, Provider.MultipleObjectsReturned):
            raise ExchangeProviderError(f"No Provider created.")
        return provider.provider

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

    def save(
        self,
        source_currency: str,
        exchange_currency: str,
        rate_value: Decimal,
        valuation_date: date
    ):
        data = {
            "source_currency": source_currency,
            "exchange_currency": exchange_currency,
            "rate_value": rate_value,
            "valuation_date": valuation_date
        }
        form = CurrencyExchangeRateForm(data=data)
        if form.is_valid():
            form.save()
        else:
            raise ExchangeCurrencyError(form.errors)


currency_exchange_repository = CurrencyExchangeRepositoryDB()
