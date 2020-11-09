from datetime import date
from typing import List

import requests
from dateutil import parser

from src.app import settings
from src.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse, CurrencyRate
from src.currency_exchange.exchange_retriever.exchange_provider import \
    ExchangeProviderInterface
from src.exceptions import ExchangeProviderError


class FixerProvider(ExchangeProviderInterface):
    endpoint = "http://data.fixer.io/api/{path}"

    def __init__(self):
        self.api_key = settings.API_KEY_FIXER
        if not self.api_key:
            raise ExchangeProviderError(
                f"Fixer IO: Required API KEY configuration"
            )

    def make_request(self, path, params):
        data = {"access_key": self.api_key}
        data.update(params)

        try:
            response = requests.get(
                self.endpoint.format(path=path),
                params=data
            )
            response.raise_for_status()
            result = response.json()
            if not result["success"]:
                raise ValueError(result["error"])
        except Exception as e:
            raise ExchangeProviderError(
                f"Error trying to get data from Fixer io: {e}"
            )

        return result

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

    def get_latest(
        self,
        currency: str,
        exchanged_currencies: List[str]
    ) -> ExchangeResponse:
        if not exchanged_currencies:
            raise ExchangeProviderError(
                f"No currencies provided"
            )
        params = {
            "base": currency,
            "symbols": ",".join(exchanged_currencies)
        }
        response = self.make_request("latest", params)
        return self.transform_response(response)

    def get_historical(
        self,
        currency: str,
        exchanged_currencies: List[str],
        valuation_date: date
    ) -> ExchangeResponse:
        if not exchanged_currencies:
            raise ExchangeProviderError(
                f"No exchanged_currencies provided"
            )
        params = {
            "base": currency,
            "symbols": ",".join(exchanged_currencies)
        }
        response = self.make_request(
            valuation_date.strftime("%Y-%m-%d"),
            params
        )
        return self.transform_response(response)
