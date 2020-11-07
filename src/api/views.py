from decimal import Decimal

from dateutil.parser import parse, ParserError
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from src.api.serializers.currency_exchange_rate import \
    CurrencyExchangeRateSerializer, CurrencyConvertResponse
from src.currency_exchange.models import CurrencyExchangeRate
from src.currency_exchange.use_cases.convert_currency import ConvertCurrency
from src.exceptions import ExchangeCurrencyDoesNotExist, CurrencyDoesNotExist


class CurrencyExchangeRateView(ListAPIView):
    queryset = CurrencyExchangeRate.objects.all()
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def validate_params(params):
        try:
            date_from = parse(params.get('date_from'))
            date_to = parse(params.get('date_to'))
        except Exception:
            raise serializers.ValidationError(
                "Required params: date_from and date_to"
            )
        return date_from, date_to

    def list(self, request, *args, **kwargs):
        date_from, date_to = self.validate_params(request.GET)
        queryset = CurrencyExchangeRate.objects.in_dates(date_from, date_to)
        serializer = CurrencyExchangeRateSerializer(queryset, many=True)
        return Response(serializer.data)


class ConvertCurrencyView(RetrieveAPIView):
    queryset = CurrencyExchangeRate.objects.all()
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, origin, target, *args, **kwargs):
        params = request.GET
        amount = params.get("amount")

        if not amount:
            raise serializers.ValidationError(
                f"Required GET param 'amount'"
            )

        try:
            currency_converted = ConvertCurrency().convert(
                origin,
                Decimal(amount),
                target
            )
        except (ExchangeCurrencyDoesNotExist, CurrencyDoesNotExist) as e:
            raise serializers.ValidationError(
                f"An error occurred while converting currency: {e}"
            )

        response = CurrencyConvertResponse(data={
            "amount": currency_converted.amount,
            "converted_amount": currency_converted.converted_amount,
            "origin_currency": currency_converted.origin,
            "target_currency": currency_converted.target
        })
        response.is_valid()
        return Response(response.data)
