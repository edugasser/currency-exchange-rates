from datetime import date
from typing import List

import requests
from dateutil import parser

from src.app.settings import API_KEY_FIXER
from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse, CurrencyRate
from src.currency_exchange.exchange_retriever.exchange_retriever import \
    ExchangeProvider
from src.exceptions import ExchangeProviderError


class FixerProvider(ExchangeProvider):
    endpoint = "http://data.fixer.io/api/{path}"

    def make_request(self, path, params):
        data = {"access_key": API_KEY_FIXER}
        data.update(params)
        try:
            response = requests.get(
                self.endpoint.format(path),
                params=data
            ).json()
        except Exception as e:
            raise ExchangeProviderError(
                f"Error trying to get data from Fixer io: {e}"
            )
        return response

    @staticmethod
    def transform_response(response):
        rates = []
        for currency, ratio in response["rates"].items():
            rates.append(CurrencyRate(currency, ratio))

        return ExchangeResponse(
            response["success"],
            parser.parse(response["date"]),
            response["base"],
            rates
        )

    def get_latest(self, currencies: List[str]) -> ExchangeResponse:
        if not currencies:
            raise ExchangeProviderError(
                f"No currencienns provided"
            )
        params = {"symbols": ",".join(currencies)}
        response = self.make_request("latest", params)
        return self.transform_response(response)

    def get_historical(self, currencies: List[str], valuation_date: date) -> ExchangeResponse:  # noqa
        if not currencies:
            raise ExchangeProviderError(
                f"No currencies provided"
            )
        params = {"symbols": ",".join(currencies)}
        response = self.make_request(
            valuation_date.strftime("%Y-%m-%d"),
            params
        )
        return self.transform_response(response)
