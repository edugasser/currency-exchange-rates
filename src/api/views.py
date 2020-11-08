import json
from decimal import Decimal

from dateutil.parser import parse
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from src.api.serializers import \
    CurrencyExchangeRateSerializer, CurrencyConvertResponse, TwrResponse, \
    TwrRequest
from src.currency_exchange.models import CurrencyExchangeRate
from src.currency_exchange.repository import currency_exchange_repository
from src.currency_exchange.use_cases.convert_currency import ConvertCurrency
from src.currency_exchange.use_cases.retrieve_currency_exchange import \
    RetrieveCurrencyExchange
from src.currency_exchange.use_cases.retrieve_twr import RetrieveTWR
from src.exceptions import ExchangeCurrencyDoesNotExist, CurrencyDoesNotExist
from src.utils import iter_days


class CurrencyExchangeRateView(ListAPIView):
    queryset = CurrencyExchangeRate.objects.all()

    def __init__(self, **kwargs):
        super(CurrencyExchangeRateView, self).__init__(**kwargs)
        self.retriever = RetrieveCurrencyExchange(currency_exchange_repository)
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
        return {
            "source_currency": origin,
            "target_currency": target,
            "rate_value": self.retriever.get(
                origin,
                target,
                day
            )
        }

    def list(self, request, *args, **kwargs):
        date_from, date_to = self.validate_params(request.GET)

        result = []
        for day in iter_days(date_from, date_to):
            for origin in self.currencies:
                for target in self.currencies:
                    if origin == target:
                        continue
                    result.append(
                        self.build_node(origin, target, day)
                    )

        return Response(result)


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
