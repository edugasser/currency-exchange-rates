from rest_framework import serializers

from src.currency_exchange.constants import DecimalPrecission
from src.currency_exchange.models import CurrencyExchangeRate


def decimal_field():
    return serializers.DecimalField(
        decimal_places=DecimalPrecission.DECIMAL_PLACES,
        max_digits=DecimalPrecission.MAX_DIGITS
    )


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    source_currency = serializers.CharField(source="source_currency.code")
    exchanged_currency = serializers.CharField(
        source="exchanged_currency.code"
    )

    class Meta:
        model = CurrencyExchangeRate
        fields = (
            "source_currency",
            "exchanged_currency",
            "valuation_date",
            "rate_value"
        )


class CurrencyConvertResponse(serializers.Serializer):
    amount = decimal_field()
    converted_amount = decimal_field()
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()

    def validate(self, attrs):
        if attrs["amount"] <= 0:
            raise serializers.ValidationError(
                "The field amount must be greather than 0"
            )
        return attrs


class ListCurrencyExchangeResponse(serializers.Serializer):
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
    valuation_date = serializers.DateField()
    rate_value = decimal_field()


class TwrResponse(serializers.Serializer):
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
    amount = decimal_field()
    twr = decimal_field()
    date_invested = serializers.DateField()


class TwrRequest(serializers.Serializer):
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
    amount = decimal_field()
    date_invested = serializers.DateField()

    def validate(self, attrs):
        if attrs["amount"] <= 0:
            raise serializers.ValidationError(
                "The field amount must be greather than 0"
            )
        return attrs
