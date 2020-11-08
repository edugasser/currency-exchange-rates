from rest_framework import serializers

from src.currency_exchange.constants import DecimalPrecission
from src.currency_exchange.models import CurrencyExchangeRate

DECIMAL_FIELD = serializers.DecimalField(
    decimal_places=DecimalPrecission.DECIMAL_PLACES,
    max_digits=DecimalPrecission.MAX_DIGITS
)


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    source_currency = serializers.CharField(source="source_currency.code")
    exchanged_currency = serializers.CharField(source="exchanged_currency.code")

    class Meta:
        model = CurrencyExchangeRate
        fields = (
            "source_currency",
            "exchanged_currency",
            "valuation_date",
            "rate_value"
        )


class CurrencyConvertResponse(serializers.Serializer):
    amount = DECIMAL_FIELD
    converted_amount = DECIMAL_FIELD
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()


class ListCurrencyExchangeResponse(serializers.Serializer):
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
    valuation_date = serializers.DateField()
    rate_value = DECIMAL_FIELD


class TwrResponse(serializers.Serializer):
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
    amount = DECIMAL_FIELD
    twr = DECIMAL_FIELD
    date_invested = serializers.DateField()


class TwrRequest(serializers.Serializer):
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
    amount = DECIMAL_FIELD
    date_invested = serializers.DateField()
