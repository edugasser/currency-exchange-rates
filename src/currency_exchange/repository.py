import abc
from datetime import date
from decimal import Decimal

from rest_framework import serializers

from src.currency_exchange.models import CurrencyExchangeRate, Provider, \
    Currency
from src.exceptions import (
    ExchangeProviderError,
    ExchangeCurrencyDoesNotExist,
    ExchangeCurrencyError
)


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


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = '__all__'


class CurrencyExchangeRepositoryDB(CurrencyExchangeRepository):

    def get_all_currencies(self):
        return Currency.objects.all().values_list('code', flat=True)

    def get_active_provider(self):
        try:
            provider = Provider.objects.get(default=True)
        except (Provider.DoesNotExist, Provider.MultipleObjectsReturned):
            raise ExchangeProviderError("No Provider created.")
        return provider.provider

    def get(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: date
    ) -> Decimal:
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

    @staticmethod
    def get_currency_from_code(currency_code):
        currency = Currency.objects.filter(code=currency_code).first()
        return currency.id if currency else None

    def save(
        self,
        source_currency: str,
        exchanged_currency: str,
        rate_value: Decimal,
        valuation_date: date
    ):

        data = {
            "source_currency": self.get_currency_from_code(source_currency),
            "exchanged_currency": self.get_currency_from_code(exchanged_currency),  # noqa
            "rate_value": rate_value,
            "valuation_date": valuation_date
        }

        form = CurrencyExchangeRateSerializer(data=data)

        if form.is_valid():
            form.save()
        else:
            raise ExchangeCurrencyError(form.errors)


currency_exchange_repository = CurrencyExchangeRepositoryDB()
