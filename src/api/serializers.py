from rest_framework import serializers

from src.currency_exchange.models import CurrencyExchangeRate


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
    amount = serializers.DecimalField(decimal_places=6, max_digits=18)
    converted_amount = serializers.DecimalField(decimal_places=6, max_digits=18)  # noqa
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()


class ListCurrencyExchangeResponse(serializers.Serializer):
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
    valuation_date = serializers.DateField()
    rate_value = serializers.DecimalField(decimal_places=6, max_digits=18)


class TwrResponse(serializers.Serializer):
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
    amount = serializers.DecimalField(decimal_places=6, max_digits=18)
    twr = serializers.DecimalField(decimal_places=6, max_digits=18)
    date_invested = serializers.DateField()


class TwrRequest(serializers.Serializer):
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
    amount = serializers.DecimalField(decimal_places=6, max_digits=18)
    date_invested = serializers.DateField()
