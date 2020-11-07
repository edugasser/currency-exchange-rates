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
    amount = serializers.DecimalField(max_digits=3, decimal_places=6)
    converted_amount = serializers.DecimalField(max_digits=3, decimal_places=6)
    origin_currency = serializers.CharField()
    target_currency = serializers.CharField()
