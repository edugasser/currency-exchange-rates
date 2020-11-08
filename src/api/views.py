from decimal import Decimal

from dateutil.parser import parse
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from src.api.serializers import \
    CurrencyConvertResponse, TwrResponse, \
    TwrRequest, ListCurrencyExchangeResponse
from src.currency_exchange.constants import DecimalPrecission
from src.currency_exchange.models import CurrencyExchangeRate
from src.currency_exchange.repository import currency_exchange_repository
from src.currency_exchange.use_cases.convert_currency import ConvertCurrency
from src.currency_exchange.use_cases.retrieve_currency_exchange_rate import \
    RetrieveCurrencyExchangeRate
from src.currency_exchange.use_cases.retrieve_twr import RetrieveTWR
from src.exceptions import ExchangeCurrencyDoesNotExist, CurrencyDoesNotExist
from src.utils import iter_days


class ListCurrencyExchangeRateView(ListAPIView):
    queryset = CurrencyExchangeRate.objects.all()

    def __init__(self, **kwargs):
        super(ListCurrencyExchangeRateView, self).__init__(**kwargs)
        self.retriever = RetrieveCurrencyExchangeRate(currency_exchange_repository)
        self.currencies = currency_exchange_repository.get_all_currencies()

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

    def build_node(self, origin, target, day):
        rate_value = self.retriever.get(
            origin,
            target,
            day
        )
        rate_value = rate_value
        return {
            "origin_currency": origin,
            "target_currency": target,
            "valuation_date": day.date(),
            "rate_value": rate_value
        }

    def list(self, request, origin, *args, **kwargs):
        date_from, date_to = self.validate_params(request.GET)

        result = []
        for day in iter_days(date_from, date_to):
            for target in self.currencies:
                if origin == target:
                    continue
                result.append(
                    self.build_node(origin, target, day)
                )
        response = ListCurrencyExchangeResponse(data=result, many=True)

        if not response.is_valid():
            raise serializers.ValidationError(response.errors)
        return Response(response.data)


class ConvertCurrencyView(RetrieveAPIView):
    queryset = CurrencyExchangeRate.objects.all()

    def retrieve(self, request, origin, target, *args, **kwargs):
        params = request.GET
        amount = params.get("amount")

        if not amount:
            raise serializers.ValidationError(
                f"Required GET param 'amount'"
            )

        try:
            currency_converted = ConvertCurrency(
                currency_exchange_repository
            ).convert(
                origin,
                Decimal(amount),
                target
            )
        except (ExchangeCurrencyDoesNotExist, CurrencyDoesNotExist) as e:
            raise serializers.ValidationError(
                f"An error occurred while converting currency: {e}"
            )

        response = CurrencyConvertResponse(data={
            "converted_amount": currency_converted.converted_amount,
            "origin_currency": currency_converted.origin,
            "target_currency": currency_converted.target,
            "amount": currency_converted.amount
        })

        if not response.is_valid():
            raise serializers.ValidationError(response.errors)

        return Response(response.data)


class TimeWeightedRateView(RetrieveAPIView):
    queryset = CurrencyExchangeRate.objects.all()

    def retrieve(self, request, origin, target, date_invested,  *args, **kwargs):  # noqa

        twr_request = TwrRequest(data={
            "origin_currency": origin,
            "target_currency": target,
            "date_invested": date_invested,
            "amount": request.GET.get("amount")
        })

        if not twr_request.is_valid():
            raise serializers.ValidationError(
                twr_request.errors
            )
        params = twr_request.data

        twr = RetrieveTWR(currency_exchange_repository).run(
            params["origin_currency"],
            params["target_currency"],
            Decimal(params["amount"]),
            parse(params["date_invested"])
        )

        response = TwrResponse(data={
            "origin_currency": params["origin_currency"],
            "target_currency": params["target_currency"],
            "date_invested": params["date_invested"],
            "amount": params["amount"],
            "twr": twr
        })

        if not response.is_valid():
            raise serializers.ValidationError(response.errors)

        return Response(response.data)
